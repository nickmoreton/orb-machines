import json
import subprocess
from dataclasses import dataclass, field


def orb_list():
    """List info about all machines."""
    data = subprocess.run(
        " ".join(["orb", "list", "--format", "json"]),
        shell=True,
        text=True,
        check=True,
        capture_output=True,
    )
    return json.loads(data.stdout)


def orb_info(orb_name):
    """Get info about a specific machine."""
    data = subprocess.run(
        " ".join(["orb", "info", orb_name, "--format", "json"]),
        shell=True,
        text=True,
        check=True,
        capture_output=True,
    )
    return json.loads(data.stdout)


@dataclass
class Machine:
    name: str = ""
    image: dict = field(default_factory=dict)
    config: dict = field(default_factory=dict)
    builtin: bool = False
    state: str = ""
    id: str = ""

    @property
    def image_distro(self):
        return self.image["distro"]

    @property
    def image_version(self):
        return self.image["version"]

    @property
    def image_arch(self):
        return self.image["arch"]

    @property
    def image_variant(self):
        return self.image["variant"]

    @property
    def config_isolated(self):
        return self.config["isolated"]

    @property
    def config_default_username(self):
        return self.config["default_username"]

    def stop(self):
        subprocess.run(
            " ".join(["orb", "stop", self.name]),
            shell=True,
            check=True,
            capture_output=True,
        )
        self.update_status()

    def start(self):
        subprocess.run(
            " ".join(["orb", "start", self.name]),
            shell=True,
            check=True,
            capture_output=True,
        )
        self.update_status()

    def update_status(self):
        data = orb_info(self.name)
        self.state = data["state"]
        return self.state


@dataclass
class OrbData:
    machines: list = field(default_factory=list)

    def __post_init__(self):
        data = orb_list()
        for machine in data:
            self.machines.append(
                Machine(
                    name=machine["name"],
                    image=machine["image"],
                    config=machine["config"],
                    builtin=machine["builtin"],
                    state=machine["state"],
                    id=machine["id"],
                )
            )
        self.machines.sort(key=lambda x: x.name)

    def create_machine(self, name, distro):
        subprocess.run(
            " ".join(["orb", "create", distro, name]),
            shell=True,
            check=True,
            # capture_output=True,
        )
        data = orb_info(name)
        self.machines.append(
            Machine(
                name=data["name"],
                image=data["image"],
                config=data["config"],
                builtin=data["builtin"],
                state=data["state"],
                id=data["id"],
            )
        )
        self.machines.sort(key=lambda x: x.name)

    def destroy_machine(self, name):
        subprocess.run(
            " ".join(["orb", "destroy", name]),
            shell=True,
            check=True,
            capture_output=True,
        )
        self.machines = [machine for machine in self.machines if machine.name != name]
        self.machines.sort(key=lambda x: x.name)
