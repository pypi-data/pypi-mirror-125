#!/usr/bin/env python
from pathlib import Path

import click

from puddl.cli.base import root
from puddl.db.alchemy import App
from . import log
from .libfs import list_repo_paths
from .repo2rows import get_df, GitLogError, as_csv


@root.command()
@click.argument('path', type=str)
def csv(path: str):
    path = Path(path).expanduser().absolute()
    print(as_csv(path))


@root.command()
@click.argument('path', type=str)
@click.option('-r', '--recursive', is_flag=True, help="Find repos recursively (by looking for .git) and index them")
def index(path: str, recursive: bool):
    path = Path(path).expanduser().absolute()
    app = App('git')
    app.engine.execute('TRUNCATE raw')

    if recursive:
        paths = list_repo_paths(path)
    else:
        paths = [path]

    for path in paths:
        try:
            df = get_df(path)
            app.df_append(df, 'raw')
            log.info(f'{path} with {len(df)} records')
        except GitLogError as e:
            log.warning(str(e))


def main():
    root(auto_envvar_prefix='PUDDL_FELIX_GIT')


if __name__ == '__main__':
    main()
