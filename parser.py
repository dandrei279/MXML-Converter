from abc import ABC, abstractmethod
from question import Question

class Parser(ABC):

    @abstractmethod
    def load_question(self, input):
        pass
