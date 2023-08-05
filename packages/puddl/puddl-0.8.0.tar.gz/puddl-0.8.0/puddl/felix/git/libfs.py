# coding by stackoverflow :>
# https://stackoverflow.com/a/53503693/241240
import os
from pathlib import Path
from typing import Iterator


def find_dirs(name, root) -> Iterator[Path]:
    for path, dirs, files in os.walk(root):
        if name in dirs:
            yield Path(path) / name


def list_repo_paths(root: Path) -> Iterator[Path]:
    return [p.parent for p in find_dirs('.git', root)]
