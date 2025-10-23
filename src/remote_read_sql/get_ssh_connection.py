import contextlib
import sys
from pathlib import Path

import paramiko
from dotenv import dotenv_values


@contextlib.contextmanager
def get_ssh_connection(ssh_config_path: Path):
    """Open ssh tunnel"""

    ssh_config_path = Path(ssh_config_path).expanduser()
    if not ssh_config_path.exists():
        raise FileNotFoundError(f"SSH config file not found at {ssh_config_path}.")

    config = dotenv_values(ssh_config_path)

    ssh_server = config["SSH_SERVER_IP"]
    ssh_user = config["SSH_USER"]
    ssh_key_path = Path(config["SSH_KEY_PATH"]).expanduser()
    remote_host = config["REMOTE_HOST"]
    local_bind_port = int(config["LOCAL_BIND_PORT"])
    remote_db_port = int(config["REMOTE_DB_PORT"])
    ssh_key_pass = config.get("SSH_KEY_PASS", None)

    for var, val in config.items():
        if var not in ["SSH_KEY_PASS"]:
            sys.stdout.write(f"{var}: {val}\n")

    client = paramiko.SSHClient()
    # client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    k = paramiko.RSAKey.from_private_key_file(str(ssh_key_path), password=ssh_key_pass)
    try:
        client.connect(hostname=ssh_server, username=ssh_user, pkey=k, port=22)
        transport = client.get_transport()
        transport.set_keepalive(10)
        transport.open_channel(
            "direct-tcpip",
            (remote_host, remote_db_port),
            ("127.0.0.1", local_bind_port),
        )
        sys.stdout.write("\nSSH tunnel established successfully.\n")
        yield client
    finally:
        client.close()
        sys.stdout.write("SSH tunnel closed.\n")
