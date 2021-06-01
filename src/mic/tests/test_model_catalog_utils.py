import os

from click.testing import CliRunner
from mic.__main__ import credentials
from mic.model_catalog_utils import get_api


def test_configure():
    runner = CliRunner()
    model_catalog_username = os.environ['MODEL_CATALOG_USERNAME_TEST']
    model_catalog_password = os.environ['MODEL_CATALOG_PASSWORD_TEST']
    result = runner.invoke(credentials, [
        "--username", model_catalog_username,
        "--password", model_catalog_password,
        "--dockerhub_username", "a",
        "--name", "pedro",
        "--profile", "testing"
    ])
    assert result.exit_code == 0


def test_get_api():
    runner = CliRunner()
    model_catalog_username = os.environ['MODEL_CATALOG_USERNAME_TEST']
    model_catalog_password = os.environ['MODEL_CATALOG_PASSWORD_TEST']
    result = runner.invoke(credentials, [
        "--username", model_catalog_username,
        "--password", model_catalog_password,
        "--dockerhub_username", "a",
        "--name", "pedro",
        "--profile", "testing"
    ])
    assert result.exit_code == 0
    api = get_api(profile="testing")
    assert api
