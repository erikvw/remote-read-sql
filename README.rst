Remote read_sql
===============

Homepage: https://github.com/erikvw/remote-read-sql

Source code: https://github.com/erikvw/remote-read-sql

Read SQL into a pandas data frame from a remote server

Installation
------------

.. code-block:: bash

    pip install remote-read-sql

Usage
-----

.. code-block:: python

    # change to your own paths
    ssh_config = Path("~/.my_ssh_config")
    my_cnf_path = Path("~/.my.cnf")
    db_name = "production"

    opts = {
        "ssh_config": ssh_config,
        "my_cnf_path": my_cnf_path,
        "db_name": db_name
    }

    df = remote_read_sql("SELECT * FROM subject_glucose", **opts)

    df.head()
