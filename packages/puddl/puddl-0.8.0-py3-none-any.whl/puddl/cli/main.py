import logging

from puddl.cli.config import config
from puddl.cli.db import db
from puddl.cli.base import root

log = logging.getLogger(__name__)

# every module defines a group. add them here.
root.add_command(config)
root.add_command(db)


def main():
    # this function is referenced in `setup.py`
    root(auto_envvar_prefix='PUDDL')


if __name__ == '__main__':
    main()
