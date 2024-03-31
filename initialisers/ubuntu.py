class Upgrade:

    distro = "ubuntu"

    sudo = True
    accept = True
    command_start = "sudo apt" if sudo else "apt"

    def __init__(self):
        self.command = f"{self.command_start} update && {self.command_start} upgrade -y"

    def get_command(self):
        return self.command


class Initialise:

    distro = "ubuntu"

    packages = [
        "git",
        "wget",
        "curl",
        "nano",
    ]

    sudo = True
    accept = True
    command_start = "sudo apt" if sudo else "apt"

    def __init__(self):
        # start of command
        cmd = f"{self.command_start} install -y"
        # add packages
        for package in self.packages:
            cmd += f" {package}"
        self.command = cmd


class Install:

    distro = "ubuntu"

    packages = {
        "docker": [
            "docker-ce",
            "docker-ce-cli",
            "containerd.io",
            "docker-buildx-plugin",
            "docker-compose-plugin",
        ]
    }

    sudo = True
    accept = True
    command_start = "sudo apt" if sudo else "apt"

    def __init__(self):
        # start of command
        cmd = f"{self.command_start} install -y"
        # add packages
        for package in self.packages["docker"]:
            cmd += f" {package}"
        self.command = cmd


class Configure:

    distro = "ubuntu"

    sudo = True
    accept = True
    command_start = "sudo apt" if sudo else "apt"

    def __init__(self):
        self.command = (
            f"{self.command_start} autoremove -y && {self.command_start} autoclean"
        )
