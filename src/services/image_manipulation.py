import subprocess
from pathlib import Path

from settings import Settings


def create_new_distributed_image(golden_image_path, new_image_id):
    cp_proc = subprocess.Popen(f"cp -ax {golden_image_path} {Settings.image_store}/{new_image_id}",
                               stdout=subprocess.PIPE, shell=True)
    cp_proc.communicate()
    return f"{Settings.image_store}/{new_image_id}"


def add_new_golden_image(system_files_path: Path, boot_dir_path: Path):
    cp_proc = subprocess.Popen(f"cp -ax {system_files_path} {boot_dir_path}", stdout=subprocess.PIPE,
                               shell=True)
    cp_proc.communicate()
