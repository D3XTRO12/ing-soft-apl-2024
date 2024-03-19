from abc import abstractmethod, ABC
from app import db

class Create(ABC):
    @abstractmethod
    def create(self, entity:db.Model): # type: ignore
        pass

class Read(ABC):

    @abstractmethod
    def find_by_name(self, name):
        pass