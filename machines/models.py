import json
import pprint
import subprocess
from dataclasses import dataclass, field
from importlib import import_module

from halo import Halo

from machines.helpers import parse_info


@dataclass
class MachineModel:

    name: str
    distro: str
    version: str
    arch: str
    state: str
    id: str

    upgrade: str = None
    initialise: str = None
    install: str = None
    configure: str = None

    def __post_init__(self):
        module = import_module(f"initialisers.{self.distro}")
        if hasattr(module, "Upgrade") and hasattr(module.Upgrade, "command"):
            m = module.Upgrade()
            self.upgrade = m.get_command()
        if hasattr(module, "Initialise") and hasattr(module.Initialise, "command"):
            self.initialise = module.Initialise().command
        if hasattr(module, "Install") and hasattr(module.Install, "command"):
            self.install = module.Install().command
        if hasattr(module, "Configure") and hasattr(module.Configure, "command"):
            self.configure = module.Configure().command

        pprint.pprint(self.upgrade)


@dataclass
class MachineRegistry:

    machines: list = field(default_factory=list)

    def __post_init__(self):
        data = subprocess.run(
            "orb list --format json",
            shell=True,
            capture_output=True,
        )
        for machine in json.loads(data.stdout):
            data = parse_info(machine, key=None)
            self._register_machine(data)

    def _sort_machines(self):
        self.machines.sort(key=lambda x: x.name)

    def _register_machine(self, data):
        self.machines.append(MachineModel(**data))
        self._sort_machines()

    def _unregister_machine(self, name):
        self.machines.remove(self.get_machine(name))
        self._sort_machines()

    def get_machine(self, name):
        return next(
            (machine for machine in self.machines if machine.name == name), None
        )

    def stop_machine(self, name):
        spinner = Halo(text="Stopping machine", spinner="dots")
        spinner.start()
        subprocess.run(
            f"orb stop {name}",
            shell=True,
            capture_output=True,
        )
        spinner.stop()
        self._update_status(name)

    def stop_all_machines(self):
        for machine in self.machines:
            self.stop_machine(machine.name)

    def start_machine(self, name):
        spinner = Halo(text="Starting machine", spinner="dots")
        spinner.start()
        subprocess.run(
            f"orb start {name}",
            shell=True,
            capture_output=True,
        )
        spinner.stop()
        self._update_status(name)

    def start_all_machines(self):
        for machine in self.machines:
            self.start_machine(machine.name)

    def destroy_all_machines(self):
        for machine in self.machines:
            self.destroy_machine(machine.name)

    def _update_status(self, name):
        data = subprocess.run(
            f"orb info {name} --format json",
            shell=True,
            capture_output=True,
        )
        data = parse_info(json.loads(data.stdout))
        machine = self.get_machine(name)
        machine.state = data["state"]

    def create_machine(self, name, distro, version, arch):
        if not self.get_machine(name):
            spinner = Halo(text="Creating machine", spinner="dots")
            spinner.start()
            # creation
            if version:
                subprocess.run(
                    f"orb create {distro}:{version} {name} -a {arch}",
                    shell=True,
                    capture_output=True,
                )
            else:
                subprocess.run(
                    f"orb create {distro} {name} -a {arch}",
                    shell=True,
                    capture_output=True,
                )
            spinner.stop()
            # registration
            info = subprocess.run(
                f"orb info {name} --format json",
                shell=True,
                capture_output=True,
            )
            data = parse_info(json.loads(info.stdout))
            self._register_machine(data)

    def destroy_machine(self, name):
        spinner = Halo(text="Destroying machine", spinner="dots")
        spinner.start()
        subprocess.run(
            f"orb delete {name} --force",
            shell=True,
            capture_output=True,
        )
        spinner.stop()
        self._unregister_machine(name)
