from abc import ABC, abstractmethod


class Genotype(ABC):

    @abstractmethod
    def toPhenotype(self):
        pass

    @abstractmethod
    def makeBabyWith(self, otherGenotype):
        pass

    @abstractmethod
    def nSwap(self, n):
        pass
