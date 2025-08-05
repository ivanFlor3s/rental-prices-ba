from abc import ABC, abstractmethod

class BaseScrapper(ABC):

    def __init__(self, url: str ):
        self.url = url

    @abstractmethod
    def process_page(self):
        pass

    @abstractmethod
    def get_soup(self):
        pass
  
