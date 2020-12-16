import shutil
from pathlib import Path
import os
from click.testing import CliRunner
from mic._utils import MIC_DIR, CONFIG_YAML_NAME, make_log_file, LOG_FILE

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"
UTILS_SANDBOX = Path(__file__).parent / RESOURCES / "_utils_test"

def test_make_log_file():
    log_folder = UTILS_SANDBOX / "log"
    no_log_folder = UTILS_SANDBOX / "no_log"

    # Create folder to run tests in
    os.mkdir(UTILS_SANDBOX)
    os.mkdir(log_folder)
    os.mkdir(no_log_folder)
    os.mkdir(log_folder / MIC_DIR)

    f = open(log_folder / MIC_DIR / LOG_FILE,"w")
    f.write("this is a log file")
    f.close()

    # Test function will abort if log already exists 
    assert make_log_file(log_folder / MIC_DIR) == True
    f = open(log_folder / MIC_DIR /LOG_FILE, "r")
    l = f.read()
    f.close()

    assert l == "this is a log file"

    # Test function will generate mic/mic.log if mic dir does not already exist
    assert make_log_file(no_log_folder/MIC_DIR) == True
    assert os.path.exists(no_log_folder / MIC_DIR / LOG_FILE)
    f = open(no_log_folder / MIC_DIR / LOG_FILE)
    l = f.read()
    f.close()
    assert l == ""




    # Delete folder once done
    #shutil.rmtree(UTILS_SANDBOX)


    assert get_outputs_mic(mic_1) == {'y_csv': {'format': 'csv', 'path': 'results/y.csv'}}
    assert get_outputs_mic(mic_empty) == {}

