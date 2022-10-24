include .env

DHCP_CONF_DST   := /etc/dhcp/dhcpd.conf
DHCP_SETUP_DST  := /etc/default/isc-dhcp-server
TFTP_CONF_DST   := /etc/default/tftpd-hpa
TFTP_SERVER_DST := $(SERVER_BOOT_FILE_LOCATION)/tftpboot


install:
	@echo "Installer is starting"
	sudo apt install isc-dhcp-server -y
	sudo apt install nfs-kernel-server -y
	sudo apt install tftpd-hpa -y
	sudo mkdir -p $(TFTP_SERVER_DST)
	sudo cp system_files/dhcpd_template $(DHCP_CONF_DST)
	sudo sed -i 's/<server_adapter_mac>/$(SERVER_ADAPTER_MAC_ADDRESS)/g' $(DHCP_CONF_DST)
	sudo sed -i 's/<address_for_server>/$(SERVER_PRIMARY_IP_ADDRESS)/g' $(DHCP_CONF_DST)
	sudo cp system_files/dhcpd_setup_template $(DHCP_SETUP_DST)
	sudo sed -i 's/<server_adapter>/$(SERVER_ADAPTER)/g' $(DHCP_SETUP_DST)
	sudo cp system_files/tftp_config_template $(TFTP_CONF_DST)
	sudo sed -i 's/<tftp_location>/$(TFTP_SERVER_DST)/g' $(TFTP_CONF_DST)
	sudo chown tftp:tftp $(TFTP_SERVER_DST)

run:
	flask run

monitor:
