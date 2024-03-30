from rich.columns import Columns


def parse_info(info, key=None):
    """Parse machine information.

    Flattens the data
    """

    if isinstance(info, dict):
        # Info is a single machine
        data = {
            "name": info.get("name"),
            "distro": info.get("image")["distro"],
            "version": info.get("image").get("version"),
            "arch": info.get("image").get("arch"),
            "state": info.get("state"),
            "id": info.get("id"),
        }

        if key:
            return data[key]

    elif isinstance(info, list):
        # Info is a list of machines
        data = []
        for machine in info:
            data.append(parse_info(machine, key=None))

        if key:
            return data[key]

    return data


def distributions():
    data = {
        "alma": ["8", "9"],
        "alpine": ["3.16", "3.17", "3.18", "3.19"],
        "arch": [],
        "centos": ["8", "9"],
        "debian": ["buster", "bullseye", "bookworm"],
        "devuan": ["beowulf", "chimaera", "daedalus"],
        "fedora": ["38", "39"],
        "gentoo": [],
        "kali": [],
        "nixos": ["23.11"],
        "openeuler": ["20.03", "22.03", "23.09"],
        "opensuse": ["15.4", "15.5"],
        "oracle": ["8", "9"],
        "rocky": ["8", "9"],
        "ubuntu": ["bionic", "focal", "jammy", "lunar", "mantic"],
        "void": [],
    }
    return data


def distro_keys():
    keys = distributions().keys()
    columns = Columns(keys, title="Distribution choices", equal=True, expand=True)
    return columns


def distro_versions(distro):
    try:
        versions = distributions()[distro]
        columns = Columns(versions, title="Version choices", equal=True, expand=True)
        return columns
    except KeyError:
        return None


def distro_default_version(distro):
    # get the last version in the list
    try:
        return distributions()[distro][-1]
    except IndexError:
        return None


# def architecture_versions():
#     data = ["arm64", "amd64"]
#     return data
