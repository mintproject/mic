import os

from click.testing import CliRunner

from mic.__main__ import skeleton, init

MODEL_NAME = "model"
PARAMETERS_2: int = 2


def test_skeleton(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    try:
        response = runner.invoke(skeleton, ["-n", MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False


def test_init(tmp_path):
    runner = CliRunner()
    os.chdir(tmp_path)
    response = runner.invoke(skeleton, ["-n", MODEL_NAME])
    component_dir = tmp_path / MODEL_NAME
    p = component_dir / "hello.txt"
    p.write_text("test")
    try:
        response = runner.invoke(init, [MODEL_NAME, "-p", PARAMETERS_2])
        assert response.exit_code == 0
    except:
        assert False

