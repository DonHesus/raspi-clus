import os
import subprocess
from pathlib import Path

from settings import Settings


def create_new_distributed_image(golden_image_path, new_image_id, hostname):
    os.mkdir(f"{Settings.image_store}/{new_image_id}")
    cp_proc = subprocess.Popen(f"cp -ax {golden_image_path}/* {Settings.image_store}/{new_image_id}",
                               stdout=subprocess.PIPE, shell=True)
    cp_proc.communicate()
    new_image_path = f"{Settings.image_store}/{new_image_id}"
    _edit_cmdline(new_image_path)
    _edit_fstab(new_image_path, hostname=hostname)

    return new_image_path


def add_new_golden_image(system_files_path: Path, boot_dir_path: Path, path_to_store: Path):
    cp_proc = subprocess.Popen(f"mkdir -p {path_to_store}", stdout=subprocess.PIPE,
                               shell=True)
    cp_proc.communicate()

    cp_proc = subprocess.Popen(f"cp -ax {system_files_path}/* {path_to_store}/", stdout=subprocess.PIPE,
                               shell=True)
    cp_proc.communicate()

    cp_proc = subprocess.Popen(f"cp -ax {boot_dir_path}/* {path_to_store}/boot/", stdout=subprocess.PIPE,
                               shell=True)
    cp_proc.communicate()


def _edit_cmdline(new_image_path):
    config_path = f"{new_image_path}/boot/cmdline.txt"
    new_img_server_path = f"{Settings.server_address}:{new_image_path}"

    with open(config_path, "rb") as cmdline:
        content = cmdline.read().decode()

    new_content = content.replace("<#SERVING_ADDRESS>", new_img_server_path)

    with open(config_path, "wb") as cmdline:
        cmdline.write(new_content.encode())


def _edit_fstab(new_image_path, hostname):
    config_path = f"{new_image_path}/etc/fstab"
    new_img_server_path = f"{Settings.server_address}:{Settings.nfs_directory}/{hostname}"

    config_content = f"""proc        	/proc       	proc	defaults    	0   	0
{new_img_server_path} /    	defaults,rw,nolock,proto=tcp,vers4.1         	0   	0
{new_img_server_path}/boot /boot/firmware	nfs 	defaults,rw,nolock,proto=tcp         	0   	1
none        	/tmp        	tmpfs   defaults    	0   	0
none        	/var/run    	tmpfs   defaults    	0   	0
none        	/var/lock   	tmpfs   defaults    	0   	0
none        	/var/tmp    	tmpfs   defaults    	0   	0"""

    with open(config_path, "wb") as fstab:
        fstab.write(config_content.encode())
