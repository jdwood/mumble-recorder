from abc import ABC, abstractmethod
from datetime import datetime

# Basic interface for arbitrary commands
class BaseCommand(ABC):

    def __init__(self, mumble, args):
        self.mumble=mumble
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
