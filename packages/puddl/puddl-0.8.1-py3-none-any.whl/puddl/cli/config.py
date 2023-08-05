import logging
import os

import click

from puddl.conf import DBConfig, PuddlRC

log = logging.getLogger(__name__)


@click.group()
def config():
    pass


@config.command()
@click.option('-f', '--force', is_flag=True)
def init(force):
    if PuddlRC.exists():
        if not force:
            raise click.ClickException(f'{PuddlRC.PATH} already exists')
        else:
            log.info(f'forcing overwrite of {PuddlRC.PATH}')
    from dotenv import load_dotenv

    load_dotenv()
    os.environ['PGAPPNAME'] = 'puddl config init'

    cfg = DBConfig()
    PuddlRC.write(dict(cfg))


@config.command()
def show():
    for k, v in DBConfig().items():
        print(f'{k}={v}')
