import os

from click.testing import CliRunner
from mic.__main__ import credentials
from mic.model_catalog_utils import get_api


def test_configure():
    runner = CliRunner()
    model_catalog = os.environ['MODEL_CATALOG_PASSWORD']
    result = runner.invoke(credentials,
                           ["--server", "https://api.models.mint.isi.edu/v1.4.0",
                            "--username", "mosorio@isi.edu",
                            "--git_username", "mintbot",
                            "--git_token", "asdfsafs",
                            "--password", model_catalog,
                            "--dockerhub_username", "a",
                            "--name", "pedro",
                            "--profile", "testing"])
    assert result.exit_code == 0


def test_get_api():
    runner = CliRunner()
    model_catalog = os.environ['MODEL_CATALOG_PASSWORD']
    result = runner.invoke(credentials,
                           ["--server", "https://api.models.mint.isi.edu/v1.4.0",
                            "--username", "mosorio@isi.edu",
                            "--git_username", "mintbot",
                            "--git_token", "asdfsafs",
                            "--password", model_catalog,
                            "--dockerhub_username", "a",
                            "--name", "pedro",
                            "--profile", "testing"])
    assert result.exit_code == 0

    api = get_api(profile="testing")
    assert api
