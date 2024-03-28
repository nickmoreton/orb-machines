import click

from machines.helpers import distributions, distro_default_version
from machines.models import MachineRegistry
from machines.views import architecture_list, distro_list, machine_list

DEFAULT_DISTRO = "ubuntu"


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = MachineRegistry()


@cli.command()
@click.pass_obj
def build(registry):
    # name
    click.echo()
    name = click.prompt("Enter a machine name")
    click.echo()

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

    # list machines
    machine_list(registry.machines)


@cli.command()
def distros():
    click.echo(distro_list())


@cli.command()
@click.pass_obj
def destroy(registry):
    if not registry.machines:
        click.echo("No machines to destroy")
        return

    machine_list(registry.machines, with_keys=True)
    index = click.prompt("Enter the index of the machine to delete")
    registry.destroy_machine(registry.machines[int(index) - 1].name)

    machine_list(registry.machines)


@cli.command()
@click.pass_obj
def list(registry):
    machine_list(registry.machines)


@cli.command()
@click.option("-a", "--all", is_flag=True)
@click.pass_obj
def stop(registry, all):
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
