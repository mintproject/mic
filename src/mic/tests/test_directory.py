import pytest
from mic.component.initialization import render_run_sh


def test_render_run_sh(tmp_path):
    sh = render_run_sh(tmp_path, inputs=0, parameters=10, outputs=2)
    print(sh)
    assert sh.exists()
