import re
import subprocess
from pathlib import Path

from settings import Settings

from src.services.communication import execute_server_command


def _generate_node_string(name, mac_address, address, boot_location: Path, server_address: str):
    NEW_RASPBERRY_DHCP_SECTION_TEMPLATE = f"""
      host {name} {{
        option root-path "{boot_location}";
        hardware ethernet {mac_address};
        option option-43 "Raspberry Pi Boot";
        option option-66 "{server_address}";
        next-server {server_address};
        fixed-address {address};
        option host-name "{name}";
      }}
    
    #<NODE_SPACE>
"""
    return NEW_RASPBERRY_DHCP_SECTION_TEMPLATE


def _generate_fstab_entries(os_id, raspberry_serial, hostname):
    fstab_entries = [f"{Settings.image_store}/{os_id} {Settings.nfs_directory}/{hostname} none defaults,bind 0 0\n",
                     f"{Settings.image_store}/{os_id}/boot {Settings.nfs_directory}/tftpboot/{raspberry_serial} none defaults,bind 0 0\n"]
    return fstab_entries


def add_new_node(raspberry_body: dict):
    _create_new_node_dir(raspberry_body["name"], raspberry_body["serial_number"])
    _add_dhcpd_entry(raspberry_body, Settings.dhcp_configuration_file, Settings.server_address, Settings.boot_location)
    _restart_services()


def _get_number_of_nodes(file: Path):
    with open(file=file, mode="rb") as dhcp_conf:
        content = dhcp_conf.read()
        matches = re.findall(r'host .* {', content.decode(), re.MULTILINE)
        return len(matches)


def _add_dhcpd_entry(raspberry_body: dict, dhcp_conf: Path, server_address: str, boot_location: Path):
    if not raspberry_body.get("name", None):
        raspberry_body["name"] = f"rpi{_get_number_of_nodes(dhcp_conf) + 1}"
    new_raspberry_section = _generate_node_string(raspberry_body["name"], raspberry_body["mac_address"],
                                                  raspberry_body["address"], boot_location, server_address)

    with open(dhcp_conf, mode="rb") as conf_file:
        content = conf_file.read()

    with open(dhcp_conf, mode="wb") as conf_file:
        decoded_content = content.decode()
        replaced = decoded_content.replace("#<NODE_SPACE>", new_raspberry_section)
        conf_file.write(replaced.encode())


def _create_new_node_dir(node_name, serial_number):
    proc = subprocess.Popen(f"sudo mkdir {Settings.nfs_directory}/{node_name}", stdout=subprocess.PIPE,
                            shell=True)
    proc.communicate()

    proc = subprocess.Popen(f"sudo mkdir {Settings.boot_location}/{serial_number}", stdout=subprocess.PIPE,
                            shell=True)

    proc.communicate()


def edit_fstab_conf(previous_os_id, os_id):

    with open(Settings.fstab_config, "rb") as fstab_conf:
        conf = fstab_conf.read()

    content = conf.decode()
    new_content = content.replace(previous_os_id, os_id)

    with open(Settings.fstab_config, "wb") as fstab_conf:
        fstab_conf.write(new_content.encode())

    _restart_services()


def add_fstab_entry(os_id, raspberry_serial, hostname):
    fstab_entries = _generate_fstab_entries(os_id, raspberry_serial, hostname)

    with open(Settings.fstab_config, "rb") as fstab_conf:
        conf = fstab_conf.read()

    content = conf.decode()
    content += f"{''.join(fstab_entries)}"

    with open(Settings.fstab_config, "wb") as fstab_conf:
        fstab_conf.write(content.encode())

    _restart_services()


def _restart_services():
    execute_server_command("exportfs -ra")
    execute_server_command("systemctl restart rpcbind")
    execute_server_command("systemctl restart nfs-server")
    execute_server_command("systemctl restart tftpd-hpa")
    execute_server_command("sudo mount -a")
