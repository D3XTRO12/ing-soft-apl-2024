from abc import abstractmethod, ABC
from app import db

class Create(ABC):
    @abstractmethod
    def create(self, entity:db.Model): # type: ignore
        pass

class Read(ABC):
    @abstractmethod
    def find_by_id(self, id:int):
        pass
    @abstractmethod
    def find_all(self):
        pass
    
class Delete(ABC):
    @abstractmethod
    def delete(self, entity:db.Model, id:int): # type: ignore
        pass
