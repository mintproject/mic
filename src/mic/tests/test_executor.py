import os
import re
import shutil
from pathlib import Path

from click.testing import CliRunner
from mic.component.initialization import create_base_directories
from mic.constants import MIC_DIR, CONFIG_YAML_NAME

from mic.component.executor import get_command_line

from mic.publisher.model_catalog import create_model_catalog_resource

RESOURCES = "resources"

def test_get_command_line(tmp_path):
    """
    Test case for auto configuration and yaml comment persistence

    :param tmp_path:
    :return:
    """
    test_name = "topoflow_dt"
    temp_test = tmp_path / test_name
    mic_dir = temp_test / MIC_DIR
    repository_test = Path(__file__).parent / RESOURCES / test_name
    shutil.copytree(repository_test, temp_test)
    resource = create_model_catalog_resource(mic_dir / CONFIG_YAML_NAME, test_name, None, False)
    line = get_command_line(resource)
    assert "2014-08-01 00:00:00" in line
