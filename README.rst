Remote read_sql
===============

Read SQL into a pandas data frame from a remote server

Installation
------------

.. code-block:: bash

    pip install remote-read-sql

Usage
-----

In this example, `remote_read_sql` opens an ssh tunnel and connects to the mysql server locally on port 3306. The SQL query is sanitized and passed to pandas `read_sql`.

After reading the data into the dataframe, the ssh and db connections are closed.

Preparing your credentials
++++++++++++++++++++++++++

.. code-block:: python

    # change to your own paths
    ssh_config = Path("~/.my_ssh_config")
    my_cnf_path = Path("~/.my.cnf")
    db_name = "my_database"

    # combine kwargs into a dictionary
    conn_opts = {
        "ssh_config_path": ssh_config,
        "my_cnf_path": my_cnf_path,
        "my_cnf_connection_name": "remote_server",
        "db_name": db_name,
    }

Running a single query
++++++++++++++++++++++

.. code-block:: python

    # open ssh, open db, read sql into dataframe, close db, close ssh
    df = remote_read_sql("SELECT * FROM subject_glucose", **conn_opts)

    # inspect the dataframe
    df.head()


Running multiple queries
++++++++++++++++++++++++


You can use `remote_read_sql` as a context manager to open a connection and run multiple queries.

For this to work, the SQL query is not passed to `remote_read_sql`:

.. code-block:: python

    with  remote_read_sql(**conn_opts) as db_conn:
        df_glucose = pd.read_sql("SELECT * FROM subject_glucose", db_conn)
        df_bp = pd.read_sql("SELECT * FROM subject_bp", db_conn)

    df_glucose.head()
    df_bp.head()
