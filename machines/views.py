from rich.console import Console
from rich.table import Table

from machines.helpers import distributions


def machine_list(machines, with_keys=False):
    if not machines:
        console = Console()
        console.print("No machines to show")
        return

    console = Console()
    console.print()  # blank line

    table = Table(title="OrbStack Machines")
    table.add_column("Name")
    table.add_column("Distro")
    table.add_column("State")

    if not with_keys:
        for machine in machines:
            table.add_row(
                machine.name,
                f"{machine.distro}:{machine.version}:{machine.arch}",
                (
                    f"[green]{machine.state}[/green]"
                    if machine.state == "running"
                    else f"[red]{machine.state}[/red]"
                ),
            )
    else:
        table.add_column("Index")
        for i, machine in enumerate(machines, start=1):
            table.add_row(
                machine.name,
                f"{machine.distro}:{machine.version}:{machine.arch}",
                (
                    f"[green]{machine.state}[/green]"
                    if machine.state == "running"
                    else f"[red]{machine.state}[/red]"
                ),
                str(i),
            )
    console.print(table)


def distro_list(distro=None):
    console = Console()
    console.print()  # blank line

    table = Table(title="OrbStack Distributions")
    table.add_column("Distribution")
    table.add_column("Versions")

    if distro:
        table.add_row(distro, ", ".join(distributions()[distro]))
        console.print(table)
        return

    for distro, versions in distributions().items():
        table.add_row(distro, ", ".join(versions))

    console.print(table)


def architecture_list():
    console = Console()
    console.print()  # blank line

    table = Table(title="OrbStack Architectures")
    table.add_column("Architecture")

    for arch in ["amd64", "arm64"]:
        table.add_row(arch)

    console.print(table)
