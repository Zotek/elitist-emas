
class MultiobjectiveFitness():
    def __init__(self, fitnessTuple, minimization=True):
        self.fitnessTuple = fitnessTuple
        self.minimization = minimization

    def __lt__(self, other):
        return self.__isDominated__(other) if self.minimization else self.__dominate__(other)


    def __gt__(self, other):
        return self.__dominate__(other) if self.minimization else self.__isDominated__(other)

    def __isDominated__(self,other):
        return all(map(lambda x: x[0]<=x[1],zip(self.fitnessTuple,other.fitnessTuple))) and any(map(lambda x: x[0]<x[1],zip(self.fitnessTuple,other.fitnessTuple)))

    def __dominate__(self,other):
        return all(map(lambda x: x[0]>=x[1],zip(self.fitnessTuple,other.fitnessTuple))) and any(map(lambda x: x[0]>x[1],zip(self.fitnessTuple,other.fitnessTuple)))

    def __str__(self):
        return self.fitnessTuple.__str__()

    def __abs__(self):
        return self.fitnessTuple