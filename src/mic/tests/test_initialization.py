import pytest
from mic.component.initialization import render_run_sh, create_directory


def test_create_directory(tmp_path):
    assert create_directory(tmp_path, "test").exists()
