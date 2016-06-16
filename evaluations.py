import logging
from math import sqrt, sin, pi
from pyage.core.operator import Operator
from pyage.solutions.evolution.genotype import FloatGenotype,PointGenotype
from multiobjective_fitness import MultiobjectiveFitness

logger = logging.getLogger(__name__)

class SchafferEvaluation(Operator):
    def __init__(self):
        super(SchafferEvaluation,self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__Schaffer(genotype.genes[0])

    def __Schaffer(self, x):
        return MultiobjectiveFitness(((x**2),(x-2)**2))

class ConstrExEvaluation(Operator):
    def __init__(self):
        super(ConstrExEvaluation,self).__init__(PointGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__ConstrEx(genotype.x,genotype.y)

    def __ConstrEx(self,x,y):
        if (y+9*x>=6) or (-y+9*x)>=1 or 0<x<=1 or 0<=y<=5:
            return MultiobjectiveFitness((-float("inf"),-float("inf")))
        return MultiobjectiveFitness((-x,-(1+y)/x))

class ZDTEvaluation(Operator):
    def __init__(self):
        super(ZDTEvaluation,self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__ZDT_default(genotype.genes)

    def _f(self,genes):
        return genes[0]

    def _g(self,genes):
        return 1 + (9.0/29.0)*sum(genes[1:])

    def _h(self,genes):
        raise NotImplementedError

    def __ZDT_default(self,genes):
        return self.__ZDT(self._f,self._g,self._h,genes)

    def __ZDT(self,f,g,h,genes):
        return MultiobjectiveFitness((f(genes),g(genes)*h(genes)),minimization=False)

    def getFront(self):
        front = [x*0.01 for x in range(0,100)]
        return map(lambda x: self.__ZDT(self._f,lambda g: 1, self._h,[x]),front)




class ZDT3Evaluation(ZDTEvaluation):
    def __init__(self):
        super(ZDT3Evaluation,self).__init__()

    def _h(self,genes):
        return 1 - sqrt(self._f(genes)/self._g(genes)) - (self._f(genes)/self._g(genes))*sin(10*pi*self._f(genes))

class ZDT1Evaluation(ZDTEvaluation):
    def __init__(self):
        super(ZDT1Evaluation,self).__init__()

    def _h(self,genes):
        return 1 - sqrt(self._f(genes)/self._g(genes))


class ZDT2Evaluation(ZDTEvaluation):
    def __init__(self):
        super(ZDT2Evaluation,self).__init__()

    def _h(self,genes):
        return 1 - (self._f(genes)/self._g(genes))**2


