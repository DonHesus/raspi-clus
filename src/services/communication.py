import logging
import paramiko
import subprocess

logger = logging.getLogger("raspi_clus_server")


def execute_ssh_raspberry_command(command: str, address: str, username="pi", password="raspberry"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(address, username=username, password=password, timeout=10)
    logger.info(f"Sending command: {command} to {address}")
    stdin, stdout, stderr = ssh.exec_command(command)
    logger.info(f"Output of the command: \n {stdout.read()}")


def execute_server_command(command: str):
    logger.info(f"Executing Server command: {command}")
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()

