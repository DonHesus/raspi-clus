import paramiko
import subprocess


def execute_ssh_raspberry_command(command: str, address: str, username="pi", password="raspberry"):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(address, username=username, password=password, timeout=10)
    ssh.exec_command(command)


def execute_server_command(command: str):
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    return proc.communicate()

