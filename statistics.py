import logging
import matplotlib.pyplot as plt
from pyage.core.statistics import Statistics

logger = logging.getLogger(__name__)

class MultiObjectiveStats(Statistics):
    def __init__(self, file_name='stats.txt'):
        self.plot_file_name = file_name

    def update(self, step_count, agents):
        x = filter(lambda x: x.name == "elitist",agents)[0]
        logger.info("elite agents:"+str(len(x.get_agents())))

    def summarize(self, agents):
        non_elite = filter(lambda x: x.name!="elitist",agents)
        elite = filter(lambda x: x.name=="elitist",agents)

        xs = map(lambda x: x.get_genotype(),[item for sublist in map(lambda x: x.get_agents(),non_elite) for item in sublist])
        c = ["r"] * len(xs)
        xs+=map(lambda x: x.get_genotype(),[item for sublist in map(lambda x: x.get_agents(),elite) for item in sublist])
        c += ["y"]*(len(xs)-len(c))
        points = map(lambda x: (x.fitness.fitnessTuple[0],x.fitness.fitnessTuple[1]), xs)
        x,y = zip(*points)
        logger.info(len(x))
        logger.info(len(y))
        # for x in agents:
        #     logger.info(str(x.name)+":"+str(len(x.get_agents())))
        plt.scatter(x,y,c=c)

        plt.show()

