from abc import ABC, abstractmethod


class Benchmark(ABC):

    @abstractmethod
    def run(self):
        pass