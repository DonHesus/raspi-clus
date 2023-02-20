include .env

VENV 			:= venv
PYTHON 			:= $(VENV)/bin/python

DHCP_SETUP_DST  := /etc/default/isc-dhcp-server
TFTP_CONF_DST   := /etc/default/tftpd-hpa
VENV            := venv/bin/python
GREEN           :='\033[0;32m'
NO_COLOR        :='\033[0m'

install-venv:
	python3 -m venv venv
	$(VENV) -m pip install --upgrade pip
	$(VENV) -m pip install -r requirements.txt

install-rancher:
	sudo mkdir -p /etc/rancher/rke2
	sudo cp system_files/rancher_config.yaml /etc/rancher/rke2/config.yaml
	sudo curl -sfL https://get.rancher.io | sh -
	sudo systemctl enable rancherd-server.service
	sudo systemctl start rancherd-server.service

install-k3s:
	@echo "Installing Kubernetes"
	sudo curl -sfL https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -s

setup_server:
	@echo -e ${GREEN}Setting up Server${NO_COLOR}
	@echo "Installing services"
	@sudo apt install isc-dhcp-server -y
	@sudo apt install nfs-kernel-server -y
	@sudo apt install tftpd-hpa -y
	@echo "Creating directories"
	@sudo mkdir -p $(NFS_SERVING_DIR)
	@sudo mkdir -p $(IMAGE_STORE)
	@sudo mkdir -p $(TFTP_SERVER_DST)
	@echo "Copying configs templates"
	sudo cp system_files/dhcpd_template $(DHCPD_CONF_FILE)
	sudo sed -i 's/<server_adapter_mac>/$(SERVER_ADAPTER_MAC_ADDRESS)/g' $(DHCPD_CONF_FILE)
	sudo sed -i 's/<address_for_server>/$(SERVER_ADDRESS)/g' $(DHCPD_CONF_FILE)
	sudo cp system_files/dhcpd_setup_template $(DHCP_SETUP_DST)
	sudo sed -i 's/<server_adapter>/$(SERVER_ADAPTER)/g' $(DHCP_SETUP_DST)
	sudo cp system_files/tftp_config_template $(TFTP_CONF_DST)
	sudo sed -i 's#<tftp_location>#$(TFTP_SERVER_DST)#g' $(TFTP_CONF_DST)
	sudo chown tftp:tftp $(TFTP_SERVER_DST)


install: install-k3s setup_server install-venv
	@echo -e ${GREEN}Save this token to the .env file under K3S_TOKEN${NO_COLOR}
	@sudo cat /var/lib/rancher/k3s/server/node-token

run-db:
	echo "Running DB"
	docker compose up -d
	sleep 5

stop-db:
	echo "Stopping DB"
	docker compose down

run_app:
	PYTHONPATH=${PYTHONPATH}:"$(shell pwd)/src" $(PYTHON) src/entrypoints/flask_app.py

run_test:
	PYTHONPATH=${PYTHONPATH}:"$(shell pwd)/src" $(PYTHON) src/entrypoints/cli.py