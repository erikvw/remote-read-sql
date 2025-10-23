from __future__ import annotations

import configparser
import contextlib
import sys
from pathlib import Path

import mysql.connector


@contextlib.contextmanager
def get_db_connection(
    ssh_conn,
    my_cnf_path: Path,
    local_bind_port: int | None = None,
    db_name: str | None = None,
):
    """Connect to mysql via tunnel"""

    my_cnf_path = Path(my_cnf_path).expanduser()
    if not my_cnf_path.exists():
        raise FileNotFoundError(f"my.cnf file not found at {my_cnf_path}.")

    config_file = Path(my_cnf_path)
    config = configparser.ConfigParser()
    config.read(config_file)

    db_user = config["client"]["user"]
    db_password = config["client"]["password"]
    db_host = config["client"]["host"]

    sys.stdout.write(f"\nUser: {db_user}\n")
    sys.stdout.write(f"Host: {db_host}\n")

    try:
        db_conn = mysql.connector.connect(
            host=db_host,
            port=local_bind_port or 3306,
            user=db_user,
            password=db_password,
            database=db_name,
        )
        sys.stdout.write("MySQL connection successful!\n")
        yield db_conn
    finally:
        if "db_conn" in locals() and db_conn.is_connected():
            db_conn.close()
            sys.stdout.write("MySQL connection closed.\n")
