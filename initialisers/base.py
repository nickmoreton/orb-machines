class BaseCommand:
    """Base class for all commands.

    Based around the debian apt package manager.

    Attributes:
        distro (str): The distribution the command is for.
        sudo (bool): Whether to use sudo or not.
        accept (bool): Whether to accept all prompts or not.
        command_start (str): The start of the command.
    """

    def __init__(self, *args, **kwargs):
        self.sudo = kwargs.get("sudo", True)
        self.accept = kwargs.get("accept", True)
        self.command_start = "sudo apt" if self.sudo else "apt"


class BaseUpgradeCommand(BaseCommand):
    """Base class for all upgrade commands."""

    @property
    def command(self):
        return f"{self.command_start} update && {self.command_start} upgrade {'-y' if self.accept else ''}"


class BaseInitialiseCommand(BaseCommand):
    """Base class for all initialise commands."""

    packages = []

    @property
    def command(self):
        if self.packages:
            return f"{self.command_start} install {'-y' if self.accept else ''} {' '.join(self.packages)}"


class BaseInstallCommand(BaseCommand):
    """Base class for all install commands."""

    packages = []

    @property
    def command(self):
        if self.packages:
            return f"{self.command_start} install {'-y' if self.accept else ''} {' '.join(self.packages)}"


class BaseConfigureCommand(BaseCommand):
    """Base class for all configure commands.

    Ad-hoc commands that are run after the machine has been initialised if you need them.
    """

    @property
    def command(self):
        return
