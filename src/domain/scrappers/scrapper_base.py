from abc import ABC, abstractmethod

class BaseScrapper(ABC):

    def __init__(self, url: str ):
        self.url = url

    @abstractmethod
    def get_departments(self):
        pass
    @abstractmethod
    def where_i_am(self) -> str:
        pass
