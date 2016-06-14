import logging
import random
from pyage.core.address import Addressable
from pyage.core.agent.agent import AbstractAgent
from pyage.core.agent.aggregate import get_random_move, AggregateAgent
from pyage.core.emas import EmasAgent, EmasService
from pyage.core.inject import Inject
from pyage.core.migration import ParentMigration
from pyage.solutions.evolution.genotype import FloatGenotype
from pyage.solutions.evolution.mutation import UniformFloatMutation

logger = logging.getLogger(__name__)


class ElEmasAgent(EmasAgent):
    def __init__(self, genotype, energy):
        super(ElEmasAgent, self).__init__(genotype, energy)
        self.prestige = 0
        self.elitist = False

    def step(self):
        self.steps += 1
        if self.dead:
            return
        if self.parent is None:
            print self.parent
        try:
            neighbour = self.parent.get_neighbour(self)
            if neighbour:
                if self.emas.should_die(self):
                    self.death()
                elif self.emas.should_reproduce(self, neighbour):
                    self.emas.reproduce(self, neighbour)
                else:
                    self.meet(neighbour)
            if self.emas.can_become_elitist(self):
                self.elitist = True
                self.migration.become_elitist(self)
            elif self.emas.can_migrate(self):
                self.migration.migrate(self)
            elif self.parent and self.emas.should_move(self):
                self.parent.move(self)
        except:
            logging.exception('')

    def meet(self, neighbour):
        logger.debug(str(self) + "meets" + str(neighbour))
        if self.get_fitness() > neighbour.get_fitness():
            transferred_energy = min(self.transferred_energy, neighbour.energy)
            self.energy += transferred_energy
            neighbour.add_energy(-transferred_energy)
            self.prestige+=1
        elif self.get_fitness() < neighbour.get_fitness():
            transferred_energy = min(self.transferred_energy, self.energy)
            self.energy -= transferred_energy
            neighbour.add_energy(transferred_energy)
            neighbour.prestige+=1
        if self.emas.should_die(self):
            self.death()

    def is_elitist(self):
        return self.elitist

    def get_prestige(self):
        return self.prestige


class ElEmasService(EmasService):
    @Inject("prestige_minimum")
    def __init__(self):
        super(ElEmasService, self).__init__()

    def should_reproduce(self, a1, a2):
        return not a1.is_elitist() and not a2.is_elitist() and super(ElEmasService, self).should_reproduce(a1, a2)

    def can_migrate(self, agent):
        return not agent.is_elitist() and super(ElEmasService,self).can_migrate(agent)

    def can_become_elitist(self,agent):
        return agent.get_prestige() > self.prestige_minimum

    def reproduce(self, a1, a2):
        logger.debug(str(a1) + " " + str(a2) + " reproducing!")
        energy = self.newborn_energy / 2 * 2
        a1.energy -= self.newborn_energy / 2
        a2.add_energy(-self.newborn_energy / 2)
        genotype = a1.crossover.cross(a1.genotype, a2.get_genotype())
        a1.mutation.process([genotype])
        newborn = ElEmasAgent(genotype, energy)
        a1.parent.locator.add_agent(newborn, get_random_move(a1.parent.locator.get_allowed_moves(a1)))
        a1.parent.add_agent(newborn)

class ParentMigrationWithElite(ParentMigration):
    def __get_random_aggregate(self, agent):
        siblings = filter(lambda x:x.name!="elitist" ,list(agent.parent.parent.get_agents()))
        return siblings

    def __get_elite(self,agent):
        siblings = filter(lambda x:x.name=="elitist" ,list(agent.parent.parent.get_agents()))
        return siblings[0]

    def become_elitist(self,agent):
        try:
            logger.debug("migrating!")
            aggregate = self.__get_elite(agent)
            logger.debug(aggregate.get_address())
            aggregate.add_agent(agent.parent.remove_agent(agent))
            return True
        except:
            logging.exception("")
        return False

def unnamed_agents_with_elitist(count, type):
    def factory():
        agents = {}
        for i in range(count):
            agent = type()
            agents[agent.get_address()] = agent

        agent = type("elitist")
        for child in agent.get_agents():
            agent.remove_agent(child)
        agents[agent.get_address()] = agent
        return agents

    return factory

def elemas_initializer(dims=1,energy=10, size=100, lowerbound=0.0, upperbound=1.0):
    agents = {}
    for i in range(size):
        agent = ElEmasAgent(FloatGenotype([random.uniform(lowerbound, upperbound) for _ in range(dims)]), energy)
        agents[agent.get_address()] = agent
    return agents

class UniformFloatMutationWithFix(UniformFloatMutation):
    def __init__(self,minimum,maximum):
        super(UniformFloatMutationWithFix, self).__init__()
        self.minimum = minimum
        self.maximum = maximum


    def mutate(self, genotype):
        index = random.randint(0, len(genotype.genes) - 1)
        genotype.genes[index] += random.uniform(-self.radius, self.radius)
        genotype.genes[index] = self.__fix(genotype.genes[index])

    def __fix(self,genotype):
        g = min(self.maximum,genotype)
        g = max(self.minimum,g)
        return g





