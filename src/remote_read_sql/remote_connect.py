import contextlib
from pathlib import Path

import pandas as pd

from .get_db_connection import get_db_connection
from .get_ssh_connection import get_ssh_connection


class InvalidSqlQueryError(Exception):
    pass


@contextlib.contextmanager
def remote_connect(
    *,
    ssh_config_path: Path,
    my_cnf_path: Path,
    my_cnf_connection_name: str,
    db_name: str,
) -> pd.DataFrame:
    """Connect to mysql via ssh tunnel."""
    with (
        get_ssh_connection(ssh_config_path) as local_bind_port,
        get_db_connection(
            my_cnf_path,
            local_bind_port=local_bind_port,
            connection_name=my_cnf_connection_name,
            db_name=db_name,
        ) as db_conn,
    ):
        yield db_conn
