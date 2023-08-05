from pathlib import Path

from puddl.felix.git.libfs import find_dirs


def test_find_dirs():
    dirs = list(find_dirs('.git', root=Path('~').expanduser()))
    assert len(dirs) > 0
