## model
import math
import networkx as nx

from mesa import Agent, Model        ## This is the model - how agent interact 
from mesa.time import SimultaneousActivation      #This is the scheduler - how agents are activated
from mesa.datacollection import DataCollector     #This output a Pandas file
from mesa.space import NetworkGrid        #This means the model runs on  network (high dimentional space)


def number_state(model, state):
    return sum([a.state == state for a in model.grid.get_all_cell_contents()])


def number_infected(model):
    return number_state(model, "infected")


def number_susceptible(model):
    return number_state(model, "susceptible")


def infected_list(model):
    return model.datacollector.get_model_vars_dataframe()


class InfoSpread(Model):
    """A virus model with some number of agents"""

    def __init__(self, num_nodes=10, avg_node_degree=3, rewire_prob=.1, initial_outbreak_size=1, threshold = 2,):
        self.num_nodes = num_nodes
        self.G = nx.watts_strogatz_graph(n=self.num_nodes, k= avg_node_degree, p=rewire_prob)   #G generate graph structure
        self.grid = NetworkGrid(self.G) #grid is the Masa native defintion of space: a coorindate with specified topology on which agents sits and interact
        self.schedule = SimultaneousActivation(self)
        self.initial_outbreak_size = (
            initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes
        )

        self.datacollector = DataCollector(
            {
                "Infected": number_infected,
                "Susceptible": number_susceptible,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = User(
                i,
                self,
                "susceptible",
                threshold
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)

        # Infect some nodes
        infected_nodes = self.random.sample(self.G.nodes(), self.initial_outbreak_size)
        for a in self.grid.get_cell_list_contents(infected_nodes):
            a.state = "infected"
            neighbors_nodes = self.grid.get_neighbors(a.pos)
            for n in self.grid.get_cell_list_contents(neighbors_nodes):
                n.state = 'infected'

        self.running = True
        self.datacollector.collect(self)

    def proportion_infected(self):
        try:
            return number_state(self, "infected") / self.num_nodes
        except ZeroDivisionError:
            return math.inf

    def step(self):
        self.schedule.step()    #this model updates with symoutanous schedule, meaning, 
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        ''' could experiment terminating model here too'''
        for i in range(n):
            self.step()


class User(Agent):
    def __init__(self, unique_id, model, initial_state, threshold):
        super().__init__(unique_id, model)   #super(). is to inherent agent's property. The user class is a subset of the agent class with additional properties. All the papermeter here are inherited from orginial agent class, everything is new and specific to the user class
        self.state = initial_state
        self.threshold = threshold


    def get_infected_neighbor_count(self):
        '''Count how many of neighbors are infected'''
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        infected_neighbors = 0
        for n in self.model.grid.get_cell_list_contents(neighbors_nodes):
            if n.state == 'infected':   
                infected_neighbors += 1
        return infected_neighbors

    def step(self):
        '''Calculates what the state should be in the next step'''
        # Start as the current state and modify below
        self._next_state = self.state
        if self.state == 'susceptible':
            infected_neighbors = self.get_infected_neighbor_count()
            if infected_neighbors >= self.threshold:
                self._next_state = 'infected'

    def advance(self):
        self.state = self._next_state

