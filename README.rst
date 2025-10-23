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

.. code-block:: python

    # change to your own paths
    ssh_config = Path("~/.my_ssh_config")
    my_cnf_path = Path("~/.my.cnf")
    db_name = "production"

    # combine kwargs into a dictionary
    opts = {
        "ssh_config": ssh_config,
        "my_cnf_path": my_cnf_path,
        "db_name": db_name
    }

    # open ssh, open db connection, read sql into dataframe, close connections
    df = remote_read_sql("SELECT * FROM subject_glucose", **opts)

    # inspect the dataframe
    df.head()
