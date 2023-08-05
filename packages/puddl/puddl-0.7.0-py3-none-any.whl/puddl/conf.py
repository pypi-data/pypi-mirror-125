import collections.abc
import json
import os
from pathlib import Path
from urllib.parse import urlencode

from puddl.typing import URL


class ConfigError(Exception):
    pass


class PuddlRC:
    PATH = Path.home() / '.puddlrc'

    @classmethod
    def exists(cls):
        return cls.PATH.exists()

    @classmethod
    def read(cls):
        with cls.PATH.open() as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError as e:
                raise ConfigError(
                    f'{cls.PATH}:{e.lineno} column {e.colno} char {e.pos}: {e.msg}'
                )

    @classmethod
    def write(cls, data):
        x = json.dumps(data, indent=2, sort_keys=True)
        with cls.PATH.open('w') as f:
            f.write(x)


class DBConfig(collections.abc.Mapping):
    """
    Abstracts a subset of the libpq environment variables defined by
    https://www.postgresql.org/docs/current/libpq-envars.html

    >>> puddl_root_db_config = DBConfig()
    >>> puddl_root_db_config.url
    'postgresql://puddl:aey1Ki4oaZohseWod2ri@localhost:13370/puddl?application_name=puddl'

    Given an app name, user and password are set accordingly

    >>> app_db_config = DBConfig('foo')
    >>> app_db_config.url
    'postgresql://foo:foo-aey1Ki4oaZohseWod2ri@localhost:13370/puddl?application_name=foo'
    """

    __slots__ = ['PGUSER', 'PGPASSWORD', 'PGHOST', 'PGPORT', 'PGDATABASE', 'PGAPPNAME']

    def __init__(self, name=None):
        env_vars_missing = []
        for key in self.__slots__:
            try:
                setattr(self, key, os.environ[key])
            except KeyError as e:
                key = e.args[0]
                env_vars_missing.append(key)

        conf_vars_missing = []
        if env_vars_missing:
            conf = PuddlRC.read()
            for key in env_vars_missing:
                try:
                    value = conf[key]
                    setattr(self, key, value)
                except KeyError:
                    conf_vars_missing.append(key)

        if conf_vars_missing:
            raise ConfigError(f'Missing variables: {env_vars_missing}. You may set them '
                              f'in the environment or by initializing ~/.puddlrc')
        if name is not None:
            self.PGUSER = name
            self.PGPASSWORD = '-'.join((name, self.PGPASSWORD))
            self.PGAPPNAME = name

    @property
    def url(self) -> URL:
        db_params = {
            'application_name': self.PGAPPNAME
        }
        params = urlencode(db_params)
        return f'postgresql://{self.PGUSER}:{self.PGPASSWORD}' \
               f'@{self.PGHOST}:{self.PGPORT}' \
               f'/{self.PGDATABASE}?{params}'

    def __str__(self):
        return self.PGUSER

    def __repr__(self):
        return f"DBConfig('{self.PGUSER}')"

    # implement Mapping ABC
    def keys(self):
        return self.__slots__

    def __getitem__(self, item):
        if item not in self.__slots__:
            raise KeyError
        return getattr(self, item)

    def __len__(self):
        return len(self.__slots__)

    def __iter__(self):
        return iter(self.__slots__)
