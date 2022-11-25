import yaml

from src.domain.models import OperatingSystem, Cluster, RaspberryPi


class ConfigLoader:
    def __init__(self):
        pass

    def load_from_yaml(self, config_path):
        with open(config_path, "rb") as config_file:
            content = yaml.safe_load(config_file)
        return self._translate_config(content)

    def parse_to_yaml(self):
        pass

    def _translate_config(self, content: dict):
        if content.get("cluster"):
            if content["cluster"].get("raspberry_pis"):
                raspberries = content["cluster"].pop('raspberry_pis')
                cluster = Cluster(**content["cluster"])
                raspberries_to_add = []
                for raspberry in raspberries:
                    if raspberry.get("operating_system"):
                        os = raspberry.pop("operating_system")
                        rasp = RaspberryPi(**raspberry)
                        rasp.operating_system = OperatingSystem(**os)
                        raspberries_to_add.append(rasp)
                cluster.raspberry_pis = raspberries_to_add
        return cluster
