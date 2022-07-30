from abc import ABC, abstractmethod

from models.base_player_parameters import BasePlayerParameters


class BasePlayer(ABC):
    def __init__(self, parameters: BasePlayerParameters):
        self.parameters = parameters

    @abstractmethod
    def playAthan(self):
        pass
