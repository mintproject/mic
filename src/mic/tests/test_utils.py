import shutil
from pathlib import Path
import os
from click.testing import CliRunner
from mic._utils import MIC_DIR, CONFIG_YAML_NAME, make_log_file, get_mic_logger, init_logger, LOG_FILE, log_system_info, log_variable, log_command, get_latest_version, check_mic_path, recursive_mic_search

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"
UTILS_SANDBOX = Path(__file__).parent / RESOURCES / "_utils_test"

def test_make_log_file():
    try:
        log_folder = UTILS_SANDBOX / "log"
        no_log_folder = UTILS_SANDBOX / "no_log"

        # Create folder to run tests in
        if not os.path.isdir(UTILS_SANDBOX):
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
        f = open(no_log_folder / MIC_DIR / LOG_FILE, "r")
        l = f.read()
        f.close()
        assert l == ""

        # Test custom log functions 
        logging = get_mic_logger()
        log_system_info(logging.name)
        log_command(logging, 
                    "generic_command", 
                    obj1="some_obj", 
                    field={'name': "name", 'version': "1.0"})
        logging.debug("debug info")
        test_var = 42
        log_variable(logging, test_var, "the answer")
        logging.info("info info")
        logging.warning("warning info")
      

        # Check the log file is being written to
        f = open(no_log_folder / MIC_DIR / LOG_FILE, "r")
        l = f.readline()
        m = f.readline()
        f.readline()
        f.readline()
        n = f.readline()
        o = f.readline()
        p = f.readline()
        f.close()

        assert l == "mic   _utils.py          INFO     Log file created\n"
        assert m != ""
        assert n == "mic   _utils.py          INFO     Command: {'name': 'generic_command', 'command_parameters': {'obj1': {'value': 'some_obj', 'type': 'str'}, 'field': {'value': {'name': 'name', 'version': '1.0'}, 'type': 'dict'}}}\n"
        assert o == "mic   test_utils.py      DEBUG    debug info\n"
        assert p == "mic   _utils.py          DEBUG    the answer: {'content': 42, 'type': 'int'}\n"


        #Delete folder once done
        shutil.rmtree(UTILS_SANDBOX)

    except Exception as e:
        #Delete folder if error happens
        shutil.rmtree(UTILS_SANDBOX)
        raise e

def test_dir_tools():
    try:
        
        mic_folder = UTILS_SANDBOX / "mic"
   
        # Check get latest version doesnt error
        assert get_latest_version().lower().find("error") == -1

        # Check ability to find path
        if not os.path.isdir(UTILS_SANDBOX):
          os.mkdir(UTILS_SANDBOX)

        os.mkdir(mic_folder)
    
        check_mic_path(None,False)        
   
        #Delete folder once done
        shutil.rmtree(UTILS_SANDBOX)

    except Exception as e:
        #Delete folder once done
        shutil.rmtree(UTILS_SANDBOX)
        raise e


