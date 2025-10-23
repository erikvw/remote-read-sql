from __future__ import annotations

import configparser
import contextlib
import sys
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


@contextlib.contextmanager
def get_db_connection(
    my_cnf_path: Path,
    *,
    local_bind_port: int,
    connection_name: str,
    db_name: str,
):
    """Connect to mysql via tunnel"""

    my_cnf_path = Path(my_cnf_path).expanduser()
    if not my_cnf_path.exists():
        raise FileNotFoundError(f"my.cnf file not found at {my_cnf_path}.")

    config_file = Path(my_cnf_path)
    config = configparser.ConfigParser()
    config.read(config_file)

    db_user = config[connection_name]["user"]
    db_password = config[connection_name]["password"]
    db_host = config[connection_name]["host"]

    db_password = quote_plus(db_password)

    sys.stdout.write(f"\nUser: {db_user}\n")
    sys.stdout.write(f"Host: {db_host}:{local_bind_port}\n")

    database_url = (
        f"mysql+mysqldb://{db_user}:{db_password}@{db_host}:{local_bind_port}/{db_name}"
    )
    sys.stdout.write(database_url)

    try:
        engine: Engine = create_engine(database_url)
        with engine.connect() as db_conn:
            sys.stdout.write("MySQL connection successful!\n")
            yield db_conn
    finally:
        pass
