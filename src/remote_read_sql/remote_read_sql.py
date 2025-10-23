import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.exc import OperationalError

from .get_db_connection import get_db_connection
from .get_ssh_connection import get_ssh_connection


def remote_read_sql(
    sql: str,
    *,
    ssh_config_path: Path,
    my_cnf_path: Path,
    db_name: str,
) -> pd.DataFrame:
    """Read sql query into dataframe via ssh tunnel and mysql connection."""
    df = None
    with get_ssh_connection(ssh_config_path) as ssh_conn:  # noqa: SIM117
        with get_db_connection(ssh_conn, my_cnf_path, db_name=db_name) as db_conn:
            try:
                df = pd.read_sql(sql, con=db_conn)
            except OperationalError as e:
                sys.stdout.write(f"Error executing query: {e}\n")
    return df
