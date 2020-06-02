from datetime import datetime

import pytest
from mic.component.executor import detect_news_file
from mic.constants import *


def test_detect_news_file(tmp_path):
    p0 = tmp_path / "hello0.txt"
    now = datetime.now().timestamp()
    d1 = tmp_path / "subdir"
    d1.mkdir()
    d2 = tmp_path / SRC_DIR
    d2.mkdir()
    p1 = tmp_path / "hello1.txt"
    p2 = tmp_path / "hello2.txt"
    p3 = tmp_path / "hello3.txt"
    p4 = tmp_path / "hello4.txt"
    p5 = d1 / "hello5.txt"
    p6 = d2 / "output.sh"
    p7 = tmp_path / CONFIG_YAML_NAME
    p1.write_text(" ")
    p2.write_text(" ")
    p3.write_text(" ")
    p4.write_text(" ")
    p5.write_text(" ")
    p6.write_text(" ")
    p7.write_text(OUTPUTS_KEY + ":")
    detected = detect_news_file(tmp_path, tmp_path / CONFIG_YAML_NAME, now)
