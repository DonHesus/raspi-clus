import datetime

from services import Handler


class RaspberryPiAliveHandler(Handler):

    def handle(self, raspberry_id):
        with self.manager.start() as uow:
            current_date = datetime.datetime.now()
            uow.raspberry_pis.update_last_alive(raspberry_id, current_date)

