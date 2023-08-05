# Prerequisites
- Python 3.9 (a virtual environment is recommended)
- PostgreSQL


# Usage
Easily create PostgreSQL schemas! In the following example, we create a schema
called `foo` and remember its URL, which contains the credentials of a role that
was specifically created for this schema. We then run a simple query.
```
puddl db create foo
psql $(puddl db url foo) -c 'SELECT 42 as answer'
```

List schemas and delete them:
```
puddl db ls
puddl db rm foo
```


# Installation
```
pip install --upgrade puddl[full]
```

Alternatively, if you do not need all the `puddl-*` scripts, then you can skip a
few dependencies.
```
pip install --upgrade puddl
```


# Shell Completion
The following installs completion for Bash. For other shells please refer to
[the click documentation][click-completion]):
```
mkdir -p ~/.bash/
_PUDDL_COMPLETE=bash_source puddl > ~/.bash/puddl

cat <<'EOF' >> ~/.bashrc
[[ -f ~/.bash/puddl ]] && source ~/.bash/puddl
EOF

exec $SHELL
```
[click-completion]: https://click.palletsprojects.com/en/7.x/bashcomplete/#activation-script


# Configuration
Prepare your environment and let puddl write a config file to `~/.puddlrc`.
You will need a PostgreSQL connection that provides super user privileges for
puddl to work in.
```
set -o allexport  # makes bash export all variables that get declared
PGHOST=127.0.0.1
PGPORT=5432
PGDATABASE=puddl
PGUSER=puddl
PGPASSWORD=puddl-pw
set +o allexport  # back to default behaviour

puddl config init

# check database connection
puddl db health

# initialized the database with sql functions as "puddl" user in "public" schema
puddl db init
```


# Development Setup
```
mkdir ~/puddl
git clone https://gitlab.com/puddl/puddl.git
cd ~/puddl/puddl/
pip install -e .[full,dev]
```

Run code style checks before committing
```
ln -s $(readlink -m env/dev/git-hooks/pre-commit) .git/hooks/pre-commit
```

Lower the log level to INFO to see what's happening.
```
export LOGLEVEL=info
```

Initialize the database. The command `puddl config init` will consume the `.env`
file if present in the current working directory.
```
cd ~/puddl/puddl/

# generate environment variables suitable for development
./env/dev/generate_env_file.sh > .env

# write initdb script and start postgres
./env/dev/create_database.sh

# based on the environment, write ~/.puddlrc
puddl config init

# make sure initialization was successful
puddl db health

# apply library sql functions as "puddl" user in "public" schema
puddl db init
```

Basic development workflow:
```
# hack, hack
make
```

Got `psql` installed?
```
source <(puddl db env)
psql -c '\df'
```

Try it:
```
cd puddl/felix/exif/
cat README.md

puddl db shell
```


# Writing an App
The following creates a schema `foo` and binds an engine to it:
```
from puddl.db.alchemy import App
app = App('foo')
app.engine
```


# Rsync Service
```
cat ~/.ssh/id_*.pub > $PUDDL_HOME/rsync_authorized_keys
ln -s env/dev/docker-compose.override.yml
docker-compose build && docker-compose up -d
```
