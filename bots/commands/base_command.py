from abc import *
from datetime import datetime

class BaseCommand(ABC):

    def __init__(self, args):
        self.args = args
        self.created_at = datetime.now()

    def execute(self):
        if self._validate():
            self._execute()

    @staticmethod
    @abstractmethod
    def name():
        pass

    @abstractmethod
    def _validate(self) -> bool:
        pass

    @abstractmethod
    def _execute(self):
        pass
