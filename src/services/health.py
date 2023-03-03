import datetime

from services import Handler


class RaspberryPiAliveHandler(Handler):

    def handle(self, mac_address):
        with self.manager.start() as uow:
            current_date = datetime.datetime.now()
            uow.raspberry_pis.update_last_alive(mac_address, current_date)

