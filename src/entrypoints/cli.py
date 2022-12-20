import argparse
import pathlib

from src.domain.config_loader import ConfigLoader


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=pathlib.Path, help="Path to config file.")

    args = parser.parse_args()

    loader = ConfigLoader()
    objects = loader.load_from_yaml_file(args.config)
    print(objects)

