# coding=utf-8
import logging
import os

from pyage.core import address
from pyage.core.agent.agent import unnamed_agents
from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import TorusLocator
from pyage.core.migration import ParentMigration
from pyage.core.stop_condition import StepLimitStopCondition
from pyage.solutions.evolution.crossover import SinglePointCrossover,AverageCrossover
from pyage.solutions.evolution.initializer import float_emas_initializer,emas_initializer
from pyage.solutions.evolution.mutation import NormalMutation,UniformPointMutation, UniformFloatMutation
from elemas import ParentMigrationWithElite, elemas_initializer, ElEmasService, unnamed_agents_with_elitist, \
    UniformFloatMutationWithFix
from evaluations import SchafferEvaluation,ConstrExEvaluation, ZDT3Evaluation, ZDT1Evaluation, ZDT2Evaluation
from statistics import MultiObjectiveStats


logger = logging.getLogger(__name__)



agents_count = int(os.environ['AGENTS'])
logger.debug("EMAS, %s agents", agents_count)
agents = unnamed_agents_with_elitist(agents_count, AggregateAgent)




stop_condition = lambda: StepLimitStopCondition(500)

aggregated_agents = lambda: elemas_initializer(dims=30,energy=100,size=25, lowerbound=0.0, upperbound=1.0)

emas = ElEmasService

minimal_energy = lambda: 0
reproduction_minimum = lambda: 90
migration_minimum = lambda: 120
newborn_energy = lambda: 100
transferred_energy = lambda: 40

prestige_minimum = lambda : 100


evaluation = lambda: ZDT1Evaluation()
crossover = SinglePointCrossover
mutation = lambda : UniformFloatMutationWithFix(0.0,1.0)

address_provider = address.SequenceAddressProvider

migration = ParentMigrationWithElite

locator = lambda: TorusLocator(10, 10)

stats = lambda: MultiObjectiveStats(evaluation().getFront,'fitness_%s_pyage.txt' % __name__)
