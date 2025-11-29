from abc import ABC, abstractmethod

class BaseService(ABC):
    """Ortak servis mantığı"""

    @abstractmethod
    def get_db(self):
        pass

