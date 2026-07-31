from abc import ABC, abstractmethod


class EvaluationMetric(ABC):

    @abstractmethod
    def evaluate(self, *args, **kwargs):
        pass