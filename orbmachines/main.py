import click
from rich.console import Console
from rich.table import Table

from orbmachines.models import OrbData


def machine_list(machines, with_keys=False):
    console = Console()
    console.print()
    table = Table(title="Orb Machines")
    if not with_keys:
        table.add_column("Name")
        table.add_column("Distro")
        table.add_column("Username")
        table.add_column("State")
        for machine in machines:
            table.add_row(
                machine.name,
                f"{machine.image_distro}:{machine.image_version}:{machine.image_arch}:{machine.image_variant}",
                f"{machine.config_default_username}",
                (
                    f"[green]{machine.state}[/green]"
                    if machine.state == "running"
                    else f"[red]{machine.state}[/red]"
                ),
            )
    else:
        table.add_column("Index")
        table.add_column("Name")
        table.add_column("Distro")
        table.add_column("Username")
        table.add_column("State")
        for i, machine in enumerate(machines, start=1):
            table.add_row(
                str(i),
                machine.name,
                f"{machine.image_distro}:{machine.image_version}:{machine.image_arch}:{machine.image_variant}",
                f"{machine.config_default_username}",
                (
                    f"[green]{machine.state}[/green]"
                    if machine.state == "running"
                    else f"[red]{machine.state}[/red]"
                ),
            )
    console.print(table)


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = OrbData()


@cli.command()
@click.pass_obj
def list(orb):
    machine_list(orb.machines)


@cli.command()
@click.option("--all", is_flag=True)
@click.pass_obj
def stop(orb, all):
    if all:
        for machine in orb.machines:
            machine.stop()
    else:
        machine_list(orb.machines, with_keys=True)
        index = click.prompt("Enter the index of the machine to stop")
        orb.machines[int(index) - 1].stop()

    machine_list(orb.machines)


@cli.command()
@click.option("--all", is_flag=True)
@click.pass_obj
def start(orb, all):
    if all:
        for machine in orb.machines:
            machine.start()
    else:
        machine_list(orb.machines, with_keys=True)
        index = click.prompt("Enter the index of the machine to start")
        orb.machines[int(index) - 1].start()

    machine_list(orb.machines)


@cli.command()
@click.argument("name")
@click.argument("distro")
@click.pass_obj
def create(orb, name, distro):
    orb.create_machine(name, distro)
    machine_list(orb.machines)


@cli.command()
@click.argument("name")
@click.pass_obj
def delete(orb, name):
    orb.destroy_machine(name)
    machine_list(orb.machines)
