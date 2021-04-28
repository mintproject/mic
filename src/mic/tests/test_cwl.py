from pathlib import Path

from mic.config_yaml import get_spec
from mic.cwl.cwl import get_parameters

RESOURCES = "resources"

def test_get_parameters():
    yml = "example.yml"
    spec = get_spec(Path(__file__).parent / RESOURCES / "cwl"/ yml)
    parameters = get_parameters(spec)
    assert len(parameters) == 8
