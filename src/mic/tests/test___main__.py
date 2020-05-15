from click.testing import CliRunner

from mic.__main__ import skeleton

MODEL_NAME = "model"


def test_skeleton(tmp_path):
    runner = CliRunner()
    try:
        response = runner.invoke(skeleton, ["-n", MODEL_NAME])
        assert response.exit_code == 0
    except:
        assert False
