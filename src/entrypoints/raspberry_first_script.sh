#!/usr/bin/env bash/bin/bash
sudo /bin/rm -v /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server
sudo systemctl restart ssh
/etc/init.d/ssh restart
#Add to correct cluster
#Remove script and put new cmdline