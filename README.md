# OrbStack Python CLI

This is a Python CLI for OrbStack. It allows you to interact with the OrbStack API from the command line.

## Features

- Create OrbStack machines
- Start, stop, rename and delete machines
- List machines
- SSH into machines
- Run common commands on machines to install software (##Initialisers)

## Installation

Poetry is used to manage dependencies. To install the dependencies, run:

```bash
poetry install
```

## Usage

To use the CLI, run:

```bash
poetry run m [command] [options]
```

For example, to list all machines, run:

```bash
poetry run m list
```

For an overview of all commands, run:

```bash
poetry run m --help
```

## Initialisers

Initialisers are classes that generate install commands and are run on a machine after it has been created. They are used to install software on the machine. The initialisers are located in the `initialisers` directory.

An initialiser/s can be run on a machine once it's created. The CLI will prompt you to run an initialiser if one it available for the machine distro you are using.

### Adding an Initialiser

To add an initialiser, create a new python file in the `initialisers` directory. The file should be named after the distro it is intended for. For example, an initialiser for Ubuntu should be named `ubuntu.py`

Look at the existing initialisers for examples e.g. `./initialisers/ubuntu.py`

## Todo's:

- Add more initialisers
- Add ability to create multiple machines at once, I'm thinking like docker-compose services but each service uses a dedicated machine.
