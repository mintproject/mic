import re
from pathlib import Path
from typing import List
import logging
import click
from mic.config_yaml import slugify
from mic.constants import *
import shlex
from mic._utils import get_mic_logger
import os

logging = get_mic_logger()
default_path = Path(MIC_DEFAULT_PATH)


def relative(files: List[Path], user_execution_directory):
    response = {}
    for i in files:
        path = Path(i).relative_to(user_execution_directory)
        name = slugify(str(path.name).replace('.', "_"))

        response[name] = {
            PATH_KEY: str(path),
            FORMAT_KEY: str(path.suffix).replace('.', '')
        }
    return response


def get_inputs_outputs_reprozip(spec, user_execution_directory, aggregrate=True):
    inputs = []
    inputs_outputs_ = spec[REPRO_ZIP_INPUTS_OUTPUTS] if spec[REPRO_ZIP_INPUTS_OUTPUTS] else []
    for i in inputs_outputs_:
        key_ = i[PATH_KEY]
        if default_path in Path(key_).parents:
            parts = Path(key_).relative_to(default_path).parts
            if isinstance(parts, str):
                inputs.append(key_)
            elif isinstance(parts, tuple):
                inputs.append(str(user_execution_directory / parts[0]))

    other_files_ = spec[REPRO_ZIP_OTHER_FILES] if spec[REPRO_ZIP_OTHER_FILES] else []
    for i in other_files_:
        if default_path in Path(i).parents:
            parts = Path(i).relative_to(default_path).parts
            if isinstance(parts, str):
                inputs.append(i)
            elif isinstance(parts, tuple) and aggregrate:
                inputs.append(str(user_execution_directory / parts[0]))
            elif isinstance(parts, tuple) and not aggregrate:
                inputs.append(str(user_execution_directory / Path(i).relative_to(default_path)))

    return list(set(inputs))


def get_outputs_reprozip(spec, user_execution_directory, aggregrate=False):
    """

    :param spec:
    :type spec:
    """
    outputs = []
    repro_zip_outputs = spec[OUTPUTS_KEY] if spec[OUTPUTS_KEY] else []
    for i in repro_zip_outputs:
        if default_path in Path(i).parents:
            parts = Path(i).relative_to(default_path).parts
            if isinstance(parts, str) and not aggregrate:
                outputs.append(i)
            if isinstance(parts, tuple):
                if aggregrate:
                    outputs.append(str(user_execution_directory / parts[0]))
                else:
                    outputs.append(str(user_execution_directory / Path(i).relative_to(default_path)))
    return list(set(outputs))


# Return a spec with auto generated params ignoring i/o files from reprozip trace
def get_parameters_reprozip(spec, reprozip_spec):
    run_lines = []
    for rep_run in reprozip_spec.get(REPRO_ZIP_RUNS):

        # Adds quotes around any cell that contains a space
        quoted_run = []
        for i in rep_run[REPRO_ZIP_ARGV]:
            if " " in i:
                quoted_run.append(f"\"{i}\"")
            else:
                quoted_run.append(i)

        run_lines.append(" ".join(map(str, quoted_run)))

    # Generate a list of all the code files from mic.yaml
    code_dict = spec.get(CODE_KEY)
    code_file_names = []
    for code_file in code_dict:
        code_file_names.append(code_dict.get(code_file).get(PATH_KEY))

    possible_params = 0
    old_invo_out = ""
    new_invo_out = ""
    for line in run_lines:

        # Get the start position. That is the earliest reference to a known code file. (ie: python3 mycode.py)
        start_pos = -1
        for c in code_file_names:
            tmp = line.find(c)
            if tmp != -1 and (start_pos > tmp or start_pos == -1):
                start_pos = tmp

        # auto check for parameters only if the current invocation line has a recognisable code file
        # This means the current run line is within the mic.yaml code_files
        if start_pos < 0:
            continue

        # Splits all possible parameters into a list. Ignores command line code call
        invocation_split_full = shlex.split(line[start_pos:len(line)])
        invocation_split = invocation_split_full[1:len(invocation_split_full)]
        
        formatted_invocation = []
        for i in invocation_split:
           
            is_param = True
            # huristically check if curr invocation split is file (contains one '.' 
            # and has at least one character in it)
            if i.count(".") == 1:
                tmp = i.split(".")
                for t in tmp:

                    # This removes a hyphen from the first position. That way negative floats doent get
                    # detected as files 
                    if len(t) > 0 and t[0] == "-":
                        t = t[1:]

                    if not t.isdigit():
                        logging.debug("File is not parameter: {}".format(i))
                        is_param = False

            if is_param:
                possible_params += 1
            
                
                auto_name = "param_" + str(possible_params)
                formatted_invocation.append("${" + auto_name + "}")

                spec.get(PARAMETERS_KEY).update({auto_name: {NAME_KEY: "", DEFAULT_VALUE_KEY: i,
                                                         DATATYPE_KEY: get_parameter_type(i),
                                                         DEFAULT_DESCRIPTION_KEY: ""}})
                click.echo("Adding \"{}\" from value {}".format(auto_name, i))
                logging.debug("Adding parameter: {}".format(auto_name))
            else:
                formatted_invocation.append(i)
            
        # print out user's invocation line(s) showing which vatiables have become parameters.
        new_invo_out += line[0:start_pos] + invocation_split_full[0]
        for l in formatted_invocation:
            new_invo_out = new_invo_out + " " + l + ""
        

        new_invo_out += "\n"
        old_invo_out += line + "\n"
        


    if possible_params > 0:
        click.echo("\nInvocation line(s):\n" + old_invo_out + "Become(s):\n" + new_invo_out)
        click.secho("The parameters of the model component are available in the mic.yaml file.", fg="green")
    else:
        click.secho("No parameters found", fg="green")
        logging.info("No parameters added")

    return spec


# Helper function for get_parameters_reprozip. Returns the type of a passed parameter string (int/double/str)
def get_parameter_type(parameter):
    
    # check if param is int
    try:
        int(parameter)
        return "int"
    except ValueError:
        pass

    # Check if char
    if len(parameter) == 1:
        return "char"

    # Check if boolean
    if parameter.lower() == "true" or parameter.lower() == "false":
        return "bool"

    # Check if double
    try:
        float(parameter)
        return "float"
    except ValueError:
        pass

    # Default to string
    return "str"


def generate_pre_runner(spec, user_execution_directory):
    code = ""
    paths = []
    code_items = spec[CODE_KEY] if CODE_KEY in spec and spec[CODE_KEY] else {}
    try:
        for key, file in code_items.items():
            paths.append(Path(file[PATH_KEY]))

        inputs_items = spec[INPUTS_KEY] if INPUTS_KEY in spec and spec[INPUTS_KEY] else {}
        items = inputs_items.items()
        for key, file in items:
            paths.append(Path(file[PATH_KEY]))

        for path in paths:
            parts = path.parts
            if isinstance(parts, tuple) and len(parts) > 1:
                code = f"""{code}
cp -rv {path.name} {str(path)}"""
        logging.debug("Pre runner code: {}".format(repr(code)))
        return code
    except KeyError as e:
        click.secho("Error: Malformed yaml. {} is missing expected fields".format(CONFIG_YAML_NAME),fg ="red")
        logging.error("Error: Malformed yaml")
        logging.error(e)
        click.secho(e,fg ="yellow")

        
def generate_runner(spec, user_execution_directory, mic_inputs, mic_outputs, mic_parameters):
    code = ''

    for run in spec[REPRO_ZIP_RUNS]:

        # Adds quotes around any cell that contains a space
        quoted_run = []
        for i in run[REPRO_ZIP_ARGV]:
            if " " in i:
                quoted_run.append(f"\"{i}\"")
            else:
                quoted_run.append(i)

        code_line = ' '.join(map(str, quoted_run))
        code_line = format_code(code_line, mic_inputs, mic_outputs, mic_parameters)
        dir_ = str(Path(run[REPRO_ZIP_WORKING_DIR]).relative_to(default_path))
        code = f"""{code}
pushd {dir_}
{code_line}
popd"""
    logging.debug("Runner code: {}".format(repr(code)))
    return code

  
def format_code(code, mic_inputs, mic_outputs, mic_parameters):
    """
    Replaces any reference to inputs and outputs with the variable name of the yaml reference
    Ex:
    ./my_script.py -i inp.txt -p 4 -o out.txt
    Becomes:
    ./my_script.py -i ${inp_txt} -p ${param_1} -o ${out_txt}
    Note: this works by checking if a input/output on the command like matches an i/o from the yaml
    :param code:
    :param mic_inputs:
    :param mic_outputs:
    :param mic_parameters:
    :return:
    """

    data = [mic_inputs,mic_outputs]
    code = shlex.split(code)
    new_code = []
    
    # Keep track of which keys have already been output in a warning message
    # This way the same key isnt output as a warning many times in a row
    known_bad_keys = []
    
    # prevent reusing params with same default value
    used_keys = []

    for item in code:
        edit = False
        # Appends tag to inputs and outputs
        for d in data:
            for key in d:
                try:
                    if str((d[key])['path'].lower()) == item.lower():
                        new_code.append("${" + key + "}")
                        edit = True
                except KeyError:
                    # Prevents the same bad keys from being repeated
                    if key not in known_bad_keys:
                        logging.warning("Warning: No path found for {}".format(key))
                        click.secho("No path found for: {}".format(key),fg="yellow")
                        known_bad_keys.append(key)

        if not edit:


            # appends tag to parameters
            for key in mic_parameters:
                try:
                    if (mic_parameters[key])["default_value"] == item and key not in used_keys:

                        # Check if param is a str. If it is add quotes around it
                        if (mic_parameters[key])["type"] == "str":
                            new_code.append("\"${" + key + "}\"")
                        else:
                            new_code.append("${" + key + "}")

                        used_keys.append(key)
                        edit = True
                        break
                except KeyError:
                    if key not in known_bad_keys:
                        click.secho("Warning: Could not find default value for {}. Check mic.yaml for errors".format(key),fg="yellow")
                        logging.warning("Could not check default value for: {}".format(key))
                        known_bad_keys.append(key)
        if not edit:
            new_code.append(item)


    return " ".join(new_code)


def find_code_files(spec, inputs, config_files, user_execution_directory):
    code_files = []
    for run in spec[REPRO_ZIP_RUNS]:

        if "binary" in run:
            try:
                code_files.append(str(user_execution_directory / Path(run['binary']).relative_to(default_path)))
            except ValueError:
                pass

        for _input in inputs:
            argv = run[REPRO_ZIP_ARGV] if isinstance(run[REPRO_ZIP_ARGV], list) else run[REPRO_ZIP_ARGV].split(' ')
            for arg in argv:
                files_path = Path(_input)
                if files_path.name in arg \
                        and files_path.is_file() \
                        and str(files_path) not in config_files:
                    # If file is a known executable add it to code_files. Else ask user if it is executable
                    if is_executable(files_path):
                        code_files.append(_input)
                        click.echo("Adding {} as executable".format(files_path.name))
                        logging.debug("Adding executable: {}".format(files_path.name))
    return list(set(code_files))


def is_executable(file_path):

    ext = os.path.splitext(file_path)[-1] # Only grab the extension
    print(ext)
    if ext.lower() in EXECUTABLE_EXTENSIONS:
        return True
    else:
        return False


def extract_parameters_from_command(command_line):
    regex = r"(\"[^\"]+\"|[^\s\"]+)"
    matches = re.finditer(regex, command_line, re.IGNORECASE)
    for matchNum, match in enumerate(matches, start=2):
        print(match.group())
