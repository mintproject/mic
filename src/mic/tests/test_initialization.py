import pytest
from mic.component.initialization import render_run_sh, create_base_directories


def test_create_directory(tmp_path):
    assert create_base_directories(tmp_path, interactive=False).exists()