from click.testing import CliRunner

from mic.__main__ import skeleton


def test_version(tmp_path):
    runner = CliRunner()
    try:
        runner.invoke(skeleton, input='wau wau\n')
    except:
        assert False
