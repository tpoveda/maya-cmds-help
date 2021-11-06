import os
import inspect

from . import commands
from .commands.scrape import Scrape
from . import version

__version__ = version.__version__
__all__ = ['version', 'commands', 'cli']

CACHE = None
SCRAPER = None


def get_all_command_years():
    years = list()
    root = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
    commands_path = os.path.join(root, 'mayacommands')
    for command_file in os.listdir(commands_path):
        if not os.path.isfile(os.path.join(commands_path, command_file)):
            continue
        years.append(os.path.splitext(command_file)[0])
    years.sort()

    return years


def get_commands_list(maya_version):
    command_years = get_all_command_years()
    if str(maya_version) not in command_years:
        return list()

    root = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
    commands_path = os.path.join(root, 'mayacommands', '{}.txt'.format(maya_version))
    with open(commands_path, 'r') as fh:
        lines = fh.readlines()
        return [line.rstrip() for line in lines[1:]]


def scrape(maya_version, maya_commands=None):
    """ Generic entry point for ease of use, returns maya_signatures.commands.scrape.Scraper(<input>).query
    :param maya_version: Maya version whose commands we want to scrap.
    :param maya_commands: Commands to query and return
    :return: 
    """
    global SCRAPER
    global CACHE
    if SCRAPER is None:
        SCRAPER = Scrape(**{'--mayaversion': [maya_version]})
        CACHE = SCRAPER.cached

    maya_commands = maya_commands or get_commands_list(maya_version)
    SCRAPER.query(maya_commands)
