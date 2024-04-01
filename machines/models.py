import json
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
        try:
            module = import_module(f"initialisers.{self.distro}")
            if hasattr(module, "Upgrade"):
                self.upgrade = module.Upgrade().command
            if hasattr(module, "Initialise"):
                self.initialise = module.Initialise().command
            if hasattr(module, "Install"):
                self.install = module.Install().command
            if hasattr(module, "Configure"):
                self.configure = module.Configure().command
        except ModuleNotFoundError:
            print(f"No initialiser found for {self.distro}")

    def run_upgrade(self):
        subprocess.run(f"orbctl run -m {self.name} -s '{self.upgrade}'", shell=True)

    def run_initialise(self):
        subprocess.run(f"orbctl run -m {self.name} -s '{self.initialise}'", shell=True)

    def run_install(self):
        subprocess.run(f"orbctl run -m {self.name} -s '{self.install}'", shell=True)

    def run_configure(self):
        subprocess.run(f"orbctl run -m {self.name} -s '{self.configure}'", shell=True)


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
                    f"orb create -a {arch} {distro}:{version} {name}",
                    shell=True,
                    capture_output=True,
                )
            else:
                subprocess.run(
                    f"orb create -a {arch} {distro} {name}",
                    shell=True,
                    capture_output=True,
                )
            spinner.stop()
            # registration
            info = subprocess.run(
                f"orb info -f json {name}",
                shell=True,
                capture_output=True,
            )
            data = parse_info(json.loads(info.stdout))
            self._register_machine(data)

    def destroy_machine(self, name):
        spinner = Halo(text="Destroying machine", spinner="dots")
        spinner.start()
        subprocess.run(
            f"orb delete -f {name}",
            shell=True,
            capture_output=True,
        )
        spinner.stop()
        self._unregister_machine(name)

    def upgrade_machine(self, name):
        machine = self.get_machine(name)
        machine.run_upgrade()

    def initialise_machine(self, name):
        machine = self.get_machine(name)
        machine.run_initialise()

    def install_machine(self, name):
        machine = self.get_machine(name)
        machine.run_install()

    def configure_machine(self, name):
        machine = self.get_machine(name)
        machine.run_configure()

    def open_shell(self, name):
        subprocess.run(f"ssh {name}@orb", shell=True)

    def rename_machine(self, name, new_name):
        spinner = Halo(text="Renaming machine", spinner="dots")
        spinner.start()
        subprocess.run(
            f"orb rename {name} {new_name}",
            shell=True,
            capture_output=True,
        )
        spinner.stop()
        self._update_status(new_name)
        # self._unregister_machine(name)
