import contextlib
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy.exc import OperationalError
from sqlglot import exp, parse_one

from .get_db_connection import get_db_connection
from .get_ssh_connection import get_ssh_connection


class InvalidSqlQueryError(Exception):
    pass


@contextlib.contextmanager
def remote_read_sql(
    sql_query: str | None = None,
    *,
    ssh_config_path: Path,
    my_cnf_path: Path,
    my_cnf_connection_name: str,
    db_name: str,
) -> pd.DataFrame:
    """Read sql query into dataframe via ssh tunnel and mysql connection."""
    df = None
    if sql_query:
        parsed = parse_one(sql_query, read="mysql")
        if not isinstance(parsed, exp.Select):
            raise InvalidSqlQueryError("Only SELECT statements are allowed.")
    with (
        get_ssh_connection(ssh_config_path) as local_bind_port,
        get_db_connection(
            my_cnf_path,
            local_bind_port=local_bind_port,
            connection_name=my_cnf_connection_name,
            db_name=db_name,
        ) as db_conn,
    ):
        if not sql_query:
            yield db_conn
        else:
            try:
                df = pd.read_sql(sql_query, con=db_conn)
            except OperationalError as e:
                sys.stdout.write(f"Error executing query: {e}\n")
        return df
