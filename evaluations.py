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

class ZDT3Evaluation(Operator):
    def __init__(self):
        super(ZDT3Evaluation,self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__ZDT1(genotype.genes)

    def __ZDT1(selfself, genes):
        f1 = lambda a: a[0]
        g = lambda a: 1 + (9/29)*sum(a[2:])
        h = lambda a: 1 - sqrt(f1(a)/g(a)) - (f1(a)/g(a))*sin(10*pi*f1(a))

        return MultiobjectiveFitness((f1(genes),g(genes)*h(genes)),minimization=False)

class ZDT1Evaluation(Operator):
    def __init__(self):
        super(ZDT1Evaluation,self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__ZDT1(genotype.genes)

    def __ZDT1(selfself, genes):
        f1 = lambda a: a[0]
        g = lambda a: 1 + (9/29)*sum(a[2:])
        h = lambda a: 1 - sqrt(f1(a)/g(a))

        return MultiobjectiveFitness((f1(genes),g(genes)*h(genes)),minimization=False)

class ZDT2Evaluation(Operator):
    def __init__(self):
        super(ZDT2Evaluation,self).__init__(FloatGenotype)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.__ZDT1(genotype.genes)

    def __ZDT1(selfself, genes):
        f1 = lambda a: a[0]
        g = lambda a: 1 + (9/29)*sum(a[2:])
        h = lambda a: 1 - (f1(a)/g(a))**2

        return MultiobjectiveFitness((f1(genes),g(genes)*h(genes)),minimization=False)
