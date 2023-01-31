import ipaddress
import json
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
            proc = subprocess.Popen("ip -j addr show wlo1", stdout=subprocess.PIPE, shell=True)
            output_dict = json.loads(proc.communicate()[0].decode())
            mac_address = output_dict["address"]
            post(f"{os.environ['SEVER_ADDRESS']}/health/{mac_address}")
            time.sleep(360)
        except KeyboardInterrupt:
            print("Exiting health_monitor")
            sys.exit(0)
