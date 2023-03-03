import json
import logging
import sys
import time
import subprocess
from dataclasses import dataclass
from requests import post

logger = logging.getLogger("health_monitor")
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("/var/log/health_monitor.log")
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
CONFIG_FILE = "/bin/health_monitor_config.json"


def set_config_varialbes():
    with open(CONFIG_FILE, "r") as config:
        config_dict = json.loads(config.read())
        setup = Settings(FIRST_BOOT=config_dict["first_boot"], SERVER_ADDRESS=config_dict["server_address"])

    return setup


def update_config_file(current_conf):
    current_conf.FIRST_BOOT = 0
    with open(CONFIG_FILE, "w") as config_file:
        config_file.write(json.dumps(current_conf.as_dict()))


@dataclass
class Settings:
    FIRST_BOOT: int
    SERVER_ADDRESS: str

    def as_dict(self):
        return {"first_boot": self.FIRST_BOOT,
                "server_address": self.SERVER_ADDRESS}


if __name__ == '__main__':
    try:
        config = set_config_varialbes()

        if int(config.FIRST_BOOT):
            proc = subprocess.Popen("sudo /bin/rm -v /etc/ssh/ssh_host_*;"
                                    " sudo dpkg-reconfigure openssh-server;"
                                    " sudo systemctl restart ssh;"
                                    " /etc/init.d/ssh restart",
                                    stdout=subprocess.PIPE, shell=True)
            proc.communicate()

            update_config_file(config)
    except Exception as msg:
        logger.info(f"Error {msg}")
        sys.exit(1)
    while True:
        try:
            proc = subprocess.Popen("ip -j addr show eth0", stdout=subprocess.PIPE, shell=True)
            output_dict = json.loads(proc.communicate()[0].decode())
            mac_address = output_dict[0]["address"]
            logger.info(f"Sending status to the server, address: {config.SERVER_ADDRESS}/health/{mac_address}")
            try:
                post(f"http://{config.SERVER_ADDRESS}/health/{mac_address}")
            except Exception as error:
                logger.info(f"Error occured error msg: {error.args}")
                sys.exit(0)
            time.sleep(360)
        except KeyboardInterrupt:
            logger.info("Exiting health_monitor")
            sys.exit(0)




