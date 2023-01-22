import ipaddress
import os
import sys
import time
import uuid
from dataclasses import dataclass
from dataclasses import asdict
import subprocess
from requests import post


@dataclass
class HealthStatus:
    id: uuid.UUID
    network: ipaddress.ip_address
    alive: bool

    def as_dict(self):
        return asdict(self)


if __name__ == '__main__':
    while True:
        try:
            proc = subprocess.Popen("ip -4 addr show wlo1 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'",
                                    stdout=subprocess.PIPE, shell=True)
            mac_address = proc.communicate()[0].decode('utf-8').strip()
            post(f"{os.environ['SEVER_ADDRESS']}/health/{mac_address}")
            time.sleep(360)
        except KeyboardInterrupt:
            print("Exiting health_monitor")
            sys.exit(0)
