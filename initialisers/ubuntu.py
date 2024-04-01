from initialisers.base import (
    BaseConfigureCommand,
    BaseInitialiseCommand,
    BaseInstallCommand,
    BaseUpgradeCommand,
)


class Upgrade(BaseUpgradeCommand):
    pass


class Initialise(BaseInitialiseCommand):
    packages = ["curl", "git", "htop", "nano", "wget"]


class Install(BaseInstallCommand):
    packages = ["python3", "python3-pip", "python3-venv"]


class Configure(BaseConfigureCommand):
    pass
