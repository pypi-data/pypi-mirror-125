#!/usr/bin/env python
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from pydantic import BaseModel

from puddl.felix.git import CommitParseError, log

here = Path(__file__).parent


class GitLogError(Exception):
    pass


class Record(BaseModel):
    repo_path: str
    hash: str
    dt: datetime
    file_path: str


class Commit:
    def __init__(self, txt: str):
        self._raw = txt
        self.lines = self._raw.strip().split('\n')
        self.header = self.lines[0]
        try:
            h, d, e, s = self.header.split(' ', 3)
        except ValueError:
            raise CommitParseError(f'could not parse header from "{self._raw}"')
        self.hash = h
        self.dt = datetime.fromisoformat(d)
        self.email = e
        self.subject = s
        self.paths = self.lines[1:]

    def __str__(self):
        return f'{self.header} ({len(self.paths)})'


class Repo:
    def __init__(self, path: Path):
        self.path = path
        self._log = self.get_log(author='felix')
        # records are separated by empty lines
        self._records = self._log.strip().split('\n\n')
        self.commits = []
        for rec in self._records:
            try:
                self.commits.append(Commit(rec))
            except CommitParseError as e:
                log.error(e)

    def get_log(self, author='felix'):
        cmd = ['git', 'log', '--reverse', "--pretty=format:%H %aI %cE %s", "--stat", "--name-only", "--author", author]
        try:
            return subprocess.check_output(cmd, cwd=self.path, encoding='utf-8', stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            raise GitLogError(f'{self.path}: {e.stderr}')


def iter_records(path: Path):
    repo = Repo(path)
    for commit in repo.commits:
        for file_path in commit.paths:
            yield Record(
                repo_path=str(repo.path),
                hash=commit.hash,
                dt=commit.dt,
                file_path=file_path,
            )


def get_df(path: Path):
    return pd.DataFrame(record.dict() for record in iter_records(path))


def as_csv(path: Path):
    records = iter_records(path.absolute())
    fieldnames = list(Record.schema()["properties"].keys())
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    for record in records:
        writer.writerow(record.dict())


if __name__ == '__main__':
    as_csv(Path('.'))
