from mic._schema import get_schema, get_schema_version, schemaVersion


def test_get_schema():
    assert get_schema()


def test_get_schema_version():
    assert get_schema_version() == schemaVersion
