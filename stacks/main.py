import click

from machines.helpers import distributions, distro_default_version
from machines.main import cli as machines_cli
from machines.views import distro_list


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}


@cli.command()
@click.pass_context
def build(ctx):
    """Build a stack of machines."""

    prefix = click.prompt("Enter a prefix for the stack")

    if not prefix:
        click.echo("Prefix is required")
        return

    complete = False
    stack = []

    while not complete:
        name = click.prompt(f"Enter the name of stack {len(stack)+1} machine")
        if not name:
            click.echo("Name is required")
            continue

        distro_list()
        distro = click.prompt(
            f"Enter a distro to use for {prefix}-{name} {len(stack)+1} machine",
            default="ubuntu",
        )
        if distro not in distributions():
            click.echo("Invalid distro")
            return

        if len(distributions()[distro]) == 0:
            version = None
        else:
            distro_list(distro)
            version = click.prompt(
                f"Enter the distro version to use for {prefix}-{name} {len(stack)+1} machine",
                default=distro_default_version(distro),
            )

            if version not in distributions()[distro]:
                click.echo("Invalid version")
                return

        stack.append({"name": name, "distro": distro, "version": version})

        click.echo("Stack summary")
        for i, machine in enumerate(stack, start=1):
            click.echo(
                f"{prefix}-{machine['name']} {i} {machine['distro']} {machine['version']}"
            )

        complete = click.confirm("Is the stack complete?", default=False)

    click.echo("Building stack...")
    for machine in stack:
        machines_cli.invoke(build, obj=machine)

    # num = click.prompt('Enter the number of machines in the stack', type=int)

    # if not num or num < 1 or not int(num):
    #     click.echo('Invalid number of machines')
    #     return

    # ctx.obj['num'] = num

    # for i in range(ctx.obj['num']):
    #     name = click.prompt(f'Enter the name of machine {i+1}')
    #     distro = click.prompt(f'Enter the distro of machine {i+1}')
    #     version = click.prompt(f'Enter the version of machine {i+1}')

    #     ctx.obj[f'machine_{i+1}'] = {
    #         'name': name,
    #         'distro': distro,
    #         'version': version
    #     }

    # click.echo('Building stack...')
    # click.echo(ctx.obj)
