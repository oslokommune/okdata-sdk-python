import os
import errno
from pathlib import Path


def write_to_okdata_cache(content, filename, failure_count=0):

    okdata_cache_path = Path(f"{os.environ['HOME']}/.okdata/cache")

    if failure_count == 2:
        print(f"Could not write credentials to {okdata_cache_path}/{filename}")
        return

    if okdata_cache_path.exists():
        f = open(f"{okdata_cache_path}/{filename}", "w+")
        f.write(content)
        f.close()

    else:
        create_dir(okdata_cache_path)
        write_to_okdata_cache(content, filename, failure_count + 1)


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def read_from_okdata_cache(filename):
    okdata_cache_path = Path(f"{os.environ['HOME']}/.okdata/cache")

    try:
        f = open(f"{okdata_cache_path}/{filename}", "r")
        content = f.read()
        f.close()
        return content
    except IOError:
        return


def write_file_content(file_name, path, content):
    if not Path(path).exists():
        create_dir(path)

    f = open(f"{path}/{file_name}", "w+")
    f.write(content)
    f.close()
