import os

from click.testing import CliRunner
from mic.click_encapsulate.commands import start

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

