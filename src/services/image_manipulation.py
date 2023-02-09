import subprocess
from pathlib import Path

from settings import Settings


def create_new_distributed_image(golden_image_path, new_image_id):
    cp_proc = subprocess.Popen(f"cp -ax {golden_image_path} {Settings.image_store}/{new_image_id}",
                               stdout=subprocess.PIPE, shell=True)
    cp_proc.communicate()
    
    _edit_cmdline(new_image_id)
    _edit_fstab(new_image_id)
    return f"{Settings.image_store}/{new_image_id}"


def add_new_golden_image(system_files_path: Path, boot_dir_path: Path):
    cp_proc = subprocess.Popen(f"cp -ax {system_files_path} {boot_dir_path}", stdout=subprocess.PIPE,
                               shell=True)
    cp_proc.communicate()


def _edit_cmdline(new_image_id):
    config_path = f"{Settings.server_address}:{Settings.image_store}/{new_image_id}/boot/cmdline"

    with open(config_path, "rb") as cmdline:
        content = cmdline.read().decode()

    content.replace("<#SERVING_ADDRESS>", config_path)

    with open(config_path, "wb") as cmdline:
        cmdline.write(content.encode())

def _edit_fstab(new_image_id):
    config_path = f"{Settings.server_address}:{Settings.image_store}/{new_image_id}/etc/fstab"

    config_content = """proc        	/proc       	proc	defaults    	0   	0
192.168.50.1:mnt/cluster/rpi1 /    	defaults,rw,nolock,proto=tcp,vers4.1         	0   	0
192.168.50.1:/mnt/cluster/rpi1/boot/firmware /boot/firmware	nfs 	defaults,rw,nolock,proto=tcp         	0   	1
none        	/tmp        	tmpfs   defaults    	0   	0
none        	/var/run    	tmpfs   defaults    	0   	0
none        	/var/lock   	tmpfs   defaults    	0   	0
none        	/var/tmp    	tmpfs   defaults    	0   	0"""

    with open(config_path, "wb") as fstab:
        fstab.write(config_content.encode())