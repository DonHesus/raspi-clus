import re
from pathlib import Path


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


def add_new_node(raspberry_body: dict, dhcp_conf: Path, server_address: str, boot_location: Path):
    if not raspberry_body.get("name", None):
        raspberry_body["name"] = f"rpi{_get_number_of_nodes(dhcp_conf)+1}"
    new_raspberry_section = _generate_node_string(raspberry_body["name"], raspberry_body["mac_address"],
                                                  raspberry_body["address"], boot_location, server_address)

    with open(dhcp_conf, mode="rb") as conf_file:
        content = conf_file.read()

    with open(dhcp_conf, mode="wb") as conf_file:
        decoded_content = content.decode()
        replaced = decoded_content.replace("#<NODE_SPACE>", new_raspberry_section)
        conf_file.write(replaced.encode())


def _get_number_of_nodes(file: Path):
    with open(file=file, mode="rb") as dhcp_conf:
        content = dhcp_conf.read()
        matches = re.findall(r'host .* {', content.decode(), re.MULTILINE)
        return len(matches)
