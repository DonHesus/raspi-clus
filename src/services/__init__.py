from abc import ABC, abstractmethod


class Handler(ABC):

    def __init__(self, uow_manager):
        self.manager = uow_manager

    @abstractmethod
    def handle(self, **kwargs):
        raise NotImplementedError