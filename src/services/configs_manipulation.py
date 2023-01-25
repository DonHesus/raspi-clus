import re
import subprocess
from pathlib import Path

from settings import Settings


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


def add_new_node(raspberry_body: dict):
    _create_new_node_dir(raspberry_body["name"], raspberry_body["serial_number"])
    _add_dhcpd_entry(raspberry_body, Settings.dhcp_configuration_file, Settings.server_address, Settings.boot_location)
    _add_node_to_exports(Settings.nfs_directory, raspberry_body["name"])


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


def _add_fstab_entry():
    pass


def edit_cmdline_entry():
    pass


def change_fstab_entry():
    pass


def _add_node_to_exports(nfs_directory, node_name):
    proc = subprocess.Popen(f"sudo echo \"{nfs_directory}/{node_name}"
                            f" 192.168.50.20/24(rw,sync,no_subtreee_check,no_root_squash\" >> /etc/exports")
    proc.communicate()
