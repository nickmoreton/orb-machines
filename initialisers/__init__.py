# # register all initialisers here, auto discover them from .py files in this folder

# import os
# from importlib import import_module


# upgrade: dict = {}
# initialise: dict = {}
# install: dict = {}
# configure: dict = {}


# for file in os.listdir(os.path.dirname(__file__)):
#     if (
#         file == "__init__.py"
#         or file[-3:] != ".py"
#         or file == "base.py"
#         or file == "helpers.py"
#     ):
#         continue

#     module = file[:-3]

#     try:
#         upgrade_module = import_module(f"initialisers.{module}")
#         upgrade[upgrade_module.Upgrade().distro] = upgrade_module.Upgrade()
#     except AttributeError:
#         pass

#     try:
#         initialise_module = import_module(f"initialisers.{module}")
#         initialise[initialise_module.Initialise().distro] = (
#             initialise_module.Initialise()
#         )
#     except AttributeError:
#         pass

#     try:
#         install_module = import_module(f"initialisers.{module}")
#         install[install_module.Install().distro] = install_module.Install()
#     except AttributeError:
#         pass

#     try:
#         configure_module = import_module(f"initialisers.{module}")
#         configure[configure_module.Configure().distro] = configure_module.Configure()
#     except AttributeError:
#         pass
