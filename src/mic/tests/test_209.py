import shutil
import os
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path
from tempfile import mkstemp

from click.testing import CliRunner
from mic.component.initialization import create_base_directories
from mic.config_yaml import get_parameters, get_inputs, get_configs, get_outputs_mic
from mic.click_encapsulate.commands import start
from mic.constants import MIC_DIR, CONFIG_YAML_NAME, SRC_DIR, DOCKER_DIR, DATA_DIR, GITIGNORE_FILE

RESOURCES = "resources"
mic_1 = Path(__file__).parent / RESOURCES / "mic_full.yaml"
mic_empty = Path(__file__).parent / RESOURCES / "mic_empty.yaml"

env = Environment(
    loader=PackageLoader('mic', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    trim_blocks=False,
    lstrip_blocks=False
)

def test_issue_209(tmp_path):
    """
    Tests if .gitignore is properly generated

    :param tmp_path:
    :return:
    """
    test_name = "209"
    temp_test = tmp_path / test_name
    repository_test = Path(__file__).parent / RESOURCES / test_name
    shutil.copytree(repository_test, temp_test)
    runner = CliRunner()
    os.chdir(temp_test)

    cmd_start("test209",runner)
    check_gitignore(runner)

def cmd_start(name, runner):
    try:
        result = runner.invoke(start, ["--name", name], catch_exceptions=False)
        print(result.output)
    except Exception as e:
        print(e)
        assert False
    assert result.exit_code == 0

def check_gitignore(runner):
    """
    Checks that .gitignore is created and is the same as template
    :param template:
    :param runner:
    :return:
    """
    gi_path = os.path.join(".","mic",GITIGNORE_FILE)
    template_content = ""
    gi_content = ""

    template = env.get_template(GITIGNORE_FILE)
    template_content = "{}\n".format(render_template(template=template))

    with open(gi_path, 'r') as r:
        gi_content = r.readlines()

    gi_content = "".join(gi_content)
    assert template_content == gi_content

def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    shutil.copymode(file_path, abs_path)
    shutil.remove(file_path)
    shutil.move(abs_path, file_path)

def render_template(template, **kwargs):
    return template.render(**kwargs)