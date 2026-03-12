import errno
import os
from pathlib import Path


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def write_file_content(file_name, path, content):
    if not Path(path).exists():
        create_dir(path)

    with open(f"{path}/{file_name}", "wb") as file:
        file.write(content)
