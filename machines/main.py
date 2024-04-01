import click

from machines.helpers import (
    configure_machine,
    distributions,
    distro_default_version,
    initialise_machine,
    install_machine,
    upgrade_machine,
)
from machines.models import MachineRegistry
from machines.views import architecture_list, distro_list, machine_list


@click.group()
@click.pass_context
def cli(ctx):
    """Manage OrbStack machines. A wrapper around the OrbStack client."""
    ctx.obj = MachineRegistry()


# CREATE --------------------------------------------------------------
@cli.command()
@click.option("-n", "--name", help="Name of the machine")
@click.option("-d", "--distro", help="Distro to use")
@click.option("-a", "--accept", is_flag=True, help="Accept all prompts")
@click.pass_obj
def create(registry, name, distro, accept):
    """Create a machine using a distro, version, and architecture."""

    if not name:
        # name
        click.echo()
        name = click.prompt("Enter a machine name")
        click.echo()

    if not distro:
        # distro
        distro_list()
        distro = click.prompt("Enter a distro to use", default="ubuntu")

    if distro not in distributions():
        click.echo("Invalid distro")
        return

    click.echo()

    # version
    if len(distributions()[distro]) == 0:
        version = None
    else:
        distro_list(distro)
        version = click.prompt(
            "Enter the distro version to use", default=distro_default_version(distro)
        )

        if version not in distributions()[distro]:
            click.echo("Invalid version")
            return

    click.echo()

    # arch
    architecture_list()
    arch = click.prompt("Enter the architecture to use", default="arm64")

    if arch not in ["arm64", "amd64"]:
        click.echo("Invalid architecture")
        return

    # create machine
    if not version:
        click.echo(f"About to create machine {name} with {distro} {arch}")
    else:
        click.echo(f"About to create machine {name} with {distro}:{version} {arch}")

    confirm = click.confirm("Do you want to continue?", default=True)
    if confirm:
        registry.create_machine(name, distro, version, arch)
    else:
        click.echo("Aborted")

    click.echo("Machine created successfully")

    # initialise machine
    machine = registry.get_machine(name)
    has_upgrade = machine.upgrade if hasattr(machine, "upgrade") else None
    has_initialise = machine.initialise if hasattr(machine, "initialise") else None
    has_install = machine.install if hasattr(machine, "install") else None
    has_configure = machine.configure if hasattr(machine, "configure") else None

    if not has_upgrade and not has_initialise and not has_install and not has_configure:
        return

    if has_upgrade:
        if not accept:
            upgrade = click.confirm(
                "Do you want to upgrade the machine?", default=False
            )
            if upgrade:
                upgrade_machine(registry, name)
        else:
            upgrade_machine(registry, name)

    if has_initialise:
        if not accept:
            initialise = click.confirm(
                "Do you want to initialise the machine?", default=False
            )
            if initialise:
                initialise_machine(registry, name)
        else:
            initialise_machine(registry, name)

    if has_install:
        if not accept:
            install = click.confirm(
                "Do you want to install the machine?", default=False
            )
            if install:
                install_machine(registry, name)
        else:
            install_machine(registry, name)

    if has_configure:
        if not accept:
            configure = click.confirm(
                "Do you want to configure the machine?", default=False
            )
            if configure:
                configure_machine(registry, name)
        else:
            configure_machine(registry, name)

    # list machines
    machine_list(registry.machines)


# POST CREATE ---------------------------------------------------------
@cli.command()
@click.pass_obj
def destroy(registry):
    """Destroy a machine."""
    if not registry.machines:
        click.echo("No machines to destroy")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to delete")

    if index not in [str(i) for i in range(1, len(registry.machines) + 1)]:
        click.echo("Invalid index")
        return

    registry.destroy_machine(registry.machines[int(index) - 1].name)

    machine_list(registry.machines)


@cli.command()
@click.option("-a", "--all", is_flag=True)
@click.pass_obj
def stop(registry, all):
    """Stop a machine."""
    if not registry.machines:
        click.echo("No machines to stop")
        return

    if all:
        registry.stop_all_machines()
    else:
        machine_list(registry.machines, with_keys=True)
        index = click.prompt("Enter the index of the machine to stop")
        registry.stop_machine(registry.machines[int(index) - 1].name)

    machine_list(registry.machines)


@cli.command()
@click.option("-a", "--all", is_flag=True)
@click.pass_obj
def start(registry, all):
    """Start a machine."""
    if not registry.machines:
        click.echo("No machines to start")
        return

    if all:
        registry.start_all_machines()
    else:
        machine_list(registry.machines, with_keys=True)
        index = click.prompt("Enter the index of the machine to start")
        registry.start_machine(registry.machines[int(index) - 1].name)

    machine_list(registry.machines)


@cli.command()
@click.pass_obj
def rename(registry):
    """Rename a machine."""
    if not registry.machines:
        click.echo("No machines to rename")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to rename")

    if index not in [str(i) for i in range(1, len(registry.machines) + 1)]:
        click.echo("Invalid index")
        return

    new_name = click.prompt("Enter the new name for the machine")
    registry.rename_machine(registry.machines[int(index) - 1].name, new_name)

    machine_list(registry.machines)


# ACTIONS ------------------------------------------------------------
@cli.command()
@click.pass_obj
def upgrade(registry):
    """Update & upgrade a machine"""
    if not registry.machines:
        click.echo("No machines to upgrade")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to upgrade")
    upgrade_machine(registry, registry.machines[int(index) - 1].name)
    click.echo("Machine upgraded successfully")


@cli.command()
@click.pass_obj
def initialise(registry):
    """Initialise a machine with some essential packages"""
    if not registry.machines:
        click.echo("No machines to initialise")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to initialise")
    initialise_machine(registry, registry.machines[int(index) - 1].name)
    click.echo("Machine initialised successfully")


@cli.command()
@click.pass_obj
def install(registry):
    """Install specific packages on a machine"""
    if not registry.machines:
        click.echo("No machines to install")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to install")
    install_machine(registry, registry.machines[int(index) - 1].name)
    click.echo("Machine installed successfully")


@cli.command()
@click.pass_obj
def configure(registry):
    """Configure a machine"""
    if not registry.machines:
        click.echo("No machines to configure")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to configure")
    configure_machine(registry, registry.machines[int(index) - 1].name)
    click.echo("Machine configured successfully")


# UTILS --------------------------------------------------------------
@cli.command()
@click.pass_obj
def shell(registry):
    """Open a shell in a machine"""
    if not registry.machines:
        click.echo("No machines to open a shell")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to open a shell")
    registry.open_shell(registry.machines[int(index) - 1].name)


@cli.command()
@click.pass_obj
def list(registry):
    """List all machines."""
    machine_list(registry.machines)


@cli.command()
def distros():
    """List all available distros."""
    click.echo(distro_list())
