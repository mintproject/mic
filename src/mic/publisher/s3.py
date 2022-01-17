"""Command to upload
"""
import logging
import os
import shutil
from pathlib import Path
from datetime import datetime
import click
from mic.credentials import get_credentials
from mint_upload.object_storage import Uploader
from mic.config_yaml import write_spec
from mic.constants import VERSION_KEY, MINT_COMPONENT_KEY, MINT_COMPONENT_ZIP, SRC_DIR

def new_version():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def push(model_directory: Path, mic_config_path: Path, name: str, profile):
    repository_name = name
    _version = new_version()
    write_spec(mic_config_path, VERSION_KEY, _version)
    logging.info("Compressing code")
    click.secho("Compressing your code")
    zip_file = compress_src_dir(model_directory, _version)
    url = upload_file(zip_file, profile, "components")
    write_spec(mic_config_path, MINT_COMPONENT_KEY, url)
    logging.info("Push complete: {}".format({'repository': url, 'version': _version}))
    click.secho("Repository: {}".format(url))
    click.secho("Version: {}".format(_version))

def upload_file(file_name: Path, profile, bucket_name):
    mint_auth_server = "https://auth.mint.isi.edu/auth/realms/production/protocol/openid-connect/token" 
    mint_s3_server   = "https://s3.mint.isi.edu"
    credentials = get_credentials(profile)
    username = credentials["username"]
    password = credentials["password"]
    uploader = Uploader(mint_s3_server, mint_auth_server, username, password)
    try:
        uploader.upload_file(
            str(file_name),
            bucket_name
        )
    except Exception as error:
        logging.error("Unable to upload", exc_info=True)
        exit(0)
    return f"""{mint_s3_server}/{bucket_name}/{file_name.name}"""


def compress_src_dir(model_path: Path, version: str) -> Path:
    """
    Compress the directory src and create a zip file
    """
    name = f"""{MINT_COMPONENT_ZIP}_{version}"""
    zip_file_name = model_path / name
    src_dir = model_path / SRC_DIR
    mic_component_path = model_path / f"{name}.zip"
    if mic_component_path.exists():
        os.remove(mic_component_path)
    zip_file_path = shutil.make_archive(zip_file_name.name, 'zip', root_dir=model_path.parent,
                                        base_dir=src_dir.relative_to(model_path.parent))
    shutil.move(zip_file_path, mic_component_path)
    return Path(mic_component_path)