from abc import ABC, abstractmethod


class LLMService(ABC):

    @abstractmethod
    def generate_response(self, prompt):
        pass

    @abstractmethod
    def get_model_name(self):
        pass