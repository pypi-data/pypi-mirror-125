![bench-logo](https://github.com/mlcgp/bench/blob/master/images/bench-logo.png?raw=true)

<p align="center"><b>Bench is a free, open-source command-line tool and dashboard web app for visualizing stock metrics.</b></p>

<p align="center">
  <a href="https://github.com/mlcgp/bench/blob/master/LICENSE.txt"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License: MIT"></a>
  <a href="https://pypi.org/project/bench-cli/"><img alt="Pypi Soda SQL" src="https://img.shields.io/badge/pypi-bench--cli-green"></a>
</p>

![bench-logo](https://github.com/mlcgp/bench/blob/master/images/screengrab.png?raw=true)

[TOC]

## Install Bench

Requirements:

* Python 3.9 or greater

Recommended:

```bash
$ pip install bench-cli
```

You can also install as a dependency within a virtual environment with [poetry](https://python-poetry.org/):

```bash
$ poetry add bench-cli
```

Otherwise, clone the project and in the project directory run:

```bash
$ poetry install
```

## Use Bench

### Getting Started

#### IEX Cloud

Sign up for IEX Cloud and get your API token: https://iexcloud.io/

#### PostgreSQL Database

All you need to do is create a new Postgres database - that's it!

The SQL queries and API calls are executed with ```$ bench run``` -- that's where all the magic happens. The SQL queries can be found [here](https://github.com/mlcgp/bench/tree/master/bench/sql).

### Commands

```bash
$ bench --install-completion zsh # Installs completion for the shell
$ bench --show-completion zsh # Shows completion for the shell
$ bench init # Creates the Bench directory tree at the user's home directory
$ bench init --directory "~/Desktop" # Creates the Bench directory tree at the user's home directory and at specified path
$ bench env # Activates the default .env
$ bench env --use "~/Desktop/bench/envs/.env" # Activates the .env file at the specified path
$ bench add "GOOGL" # adds symbol GOOGL to the watchlist
$ bench remove "FB" # removes symbol FB from the watchlist
$ bench watchlist # Displays a table of symbols in the watchlist
$ bench pipeline -i annual -n 10 # Executes the data pipeline for the last 10 years of annual data (-i or --interval can be annual or quarterly)
$ bench dash # Serves the Dash app at localhost:8050
```

The directory structure that ```$ bench init``` creates should look like:

```.
.
├── envs
└── logs
```

### Environment Configuration

The .env file should look like this:

```
# The ENV_PATH is created at ~/bench/envs/.env by default. This variable will also update when a path other than the default is used
ENV_PATH='path_to_env'

# PostgreSQL config
BENCH_DB_HOST=''
BENCH_DB_PORT=''
BENCH_DB_USER=''
BENCH_DB_NAME=''
BENCH_DB_PASSWORD=''

# The version can either be 'test' or 'stable'. Test will use the IEX Cloud Sandbox API and the test token
BENCH_IEX_VERSION=''
BENCH_IEX_TOKEN=''
# IEX Cloud Sandbox API key
BENCH_IEX_TEST_TOKEN=''

# Can provide a list of symbols in a comma-separated list (eg. 'AAPL,GOOGL,MSFT'), or use the add and remove commands
BENCH_WATCHLIST=''
```

## Roadmap

| Feature                                            | Completed | Priority |
| :------------------------------------------------- | --------- | -------- |
| Add option to ```$ bench dash``` to specify a port | N         | ***      |
| Data dictionary of supported metrics               | N         | ***      |
| Detailed logger and reports                        | N         | ***      |
| Tests                                              | N         | ***      |
| Add pipelines for other data sources               | N         | *        |
| Job scheduler for the pipeline                     | N         | *        |
| DMD for the database                               | N         | *        |