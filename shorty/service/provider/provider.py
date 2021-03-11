from abc import abstractmethod, ABC

class Provider(ABC):

    @abstractmethod
    def set_next(self, provider):
        pass

    @abstractmethod
    def get_shortlink(self, url: str) -> str:
        pass