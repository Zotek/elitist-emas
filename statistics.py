import logging
import matplotlib.pyplot as plt
from pyage.core.statistics import Statistics
from multiobjective_fitness import findFront
from hv import HyperVolume

logger = logging.getLogger(__name__)

class MultiObjectiveStats(Statistics):
    def __init__(self,front_fun, file_name='stats.txt'):
        self.front_fun = front_fun
        self.plot_file_name = file_name
        self.hv = HyperVolume([5,5])

    def update(self, step_count, agents):
        x = filter(lambda x: x.name == "elitist",agents)[0]
        logger.info("elite agents:"+str(len(x.get_agents())))
        if step_count % 5 == 0:
            non_elite = filter(lambda x: x.name!="elitist",agents)
            elite = filter(lambda x: x.name=="elitist",agents)
            xs = map(lambda x: x.get_genotype(),[item for sublist in map(lambda x: x.get_agents(),non_elite) for item in sublist])
            xs+=map(lambda x: x.get_genotype(),[item for sublist in map(lambda x: x.get_agents(),elite) for item in sublist])
            points = map(lambda x: x.fitness, xs)
            points = findFront(points)
            points = map(lambda x : x.fitnessTuple, points)
            hvr = self.hv.compute(points)
            logger.info("hvr = %s" % hvr)



    def summarize(self, agents):
        non_elite = filter(lambda x: x.name!="elitist",agents)
        elite = filter(lambda x: x.name=="elitist",agents)

        xs = map(lambda x: x.get_genotype(),[item for sublist in map(lambda x: x.get_agents(),non_elite) for item in sublist])
        exs=map(lambda x: x.get_genotype(),[item for sublist in map(lambda x: x.get_agents(),elite) for item in sublist])
        points = map(lambda x: x.fitness, xs)
        points = findFront(points)
        points = map(lambda x: (x.fitnessTuple[0],x.fitnessTuple[1]),points)
        x,y = zip(*points)
        plt.scatter(x,y)
        points = map(lambda x: x.fitness, exs)
        points = map(lambda x: (x.fitnessTuple[0],x.fitnessTuple[1]),points)
        x,y = zip(*points)
        plt.scatter(x,y,marker="^",c="r")
        x,y = zip(*map(lambda x: (x.fitnessTuple[0],x.fitnessTuple[1]),self.front_fun()))
        plt.scatter(x,y,marker="+")
        plt.show()

