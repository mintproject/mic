from mic.cli_docs import info_end_publish


def test_info_end_publish():
    info_end_publish("a", "b", "c", "default")
    info_end_publish("//!!@!  asda //", "b", "c", "default")
