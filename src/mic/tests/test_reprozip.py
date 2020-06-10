from pathlib import Path

from component.reprozip import get_outputs
from mic.config_yaml import get_spec

RESOURCES = "resources"


def test_get_outputs():
    outputs = ["/tmp/mint/TxtInOut/output.rsv", "/tmp/mint/TxtInOut/output.rch", "/tmp/mint/TxtInOut/output.sub",
               "/tmp/mint/TxtInOut/hyd.out", "/tmp/mint/TxtInOut/chan.deg", "/tmp/mint/TxtInOut/bmp-sedfil.out",
               "/tmp/mint/TxtInOut/septic.out", "/tmp/mint/TxtInOut/bmp-ri.out", "/tmp/mint/TxtInOut/output.sed",
               "/tmp/mint/TxtInOut/output.std", "/tmp/mint/TxtInOut/output.hru", "/tmp/mint/TxtInOut/input.std",
               "/tmp/mint/TxtInOut/fin.fin", "/tmp/mint/TxtInOut/watout.dat"]
    yml = "swat_test.yml"
    spec = get_spec(Path(__file__).parent / RESOURCES / yml)
    get_outputs(spec)
    assert outputs == get_outputs(spec)
