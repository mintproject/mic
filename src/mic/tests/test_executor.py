from datetime import datetime

import pytest
from mic.component.executor import detect_news_file


def test_detect_news_file(tmp_path):
    p0 = tmp_path / "hello0.txt"
    now = datetime.now().timestamp()
    d1 = tmp_path / "subdir"
    d1.mkdir()
    p1 = tmp_path / "hello1.txt"
    p2 = tmp_path / "hello2.txt"
    p3 = tmp_path / "hello3.txt"
    p4 = tmp_path / "hello4.txt"
    p5 = d1 / "hello5.txt"
    p1.write_text(" ")
    p2.write_text(" ")
    p3.write_text(" ")
    p4.write_text(" ")
    p5.write_text(" ")
    detected = detect_news_file(tmp_path, now)
