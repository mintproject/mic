import os

from click.testing import CliRunner
from mic.click_encapsulate.commands import start

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

MODEL_NAME = "model"
PARAMETERS_2: int = 2


def test_step1(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    try:
        response = runner.invoke(start, ["--name", MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False
