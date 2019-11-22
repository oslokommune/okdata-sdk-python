import os
import errno
from pathlib import Path


def write_to_origo_cache(content, filename, failure_count=0):

    origo_cache_path = Path(f"{os.environ['HOME']}/.origo/cache")

    if failure_count == 2:
        print(f"Could not write credentials to {origo_cache_path}/{filename}")
        return

    if origo_cache_path.exists():
        f = open(f"{origo_cache_path}/{filename}", "w+")
        f.write(content)
        f.close()

    else:
        create_dir(origo_cache_path)
        write_to_origo_cache(content, filename, failure_count + 1)


def create_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


def read_from_origo_cache(filename):
    origo_cache_path = Path(f"{os.environ['HOME']}/.origo/cache")

    try:
        f = open(f"{origo_cache_path}/{filename}", "r")
        content = f.read()
        f.close()
        return content
    except IOError:
        return
