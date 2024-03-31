class Initialise:

    distro = "centos"

    packages = [
        "git",
        "wget",
        "curl",
        "nano",
    ]

    sudo = True
    accept = True
    command_start = "sudo yum" if sudo else "yum"

    def update(self):
        return f"{self.command_start} check-update"

    def upgrade(self):
        return f"{self.command_start} update"


class Install:
    distro = "centos"
