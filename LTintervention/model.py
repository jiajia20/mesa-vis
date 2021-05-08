## model
import math
import networkx as nx

from mesa import Agent, Model        ## This is the model - how agent interact 
from mesa.time import SimultaneousActivation      #This is the scheduler - how agents are activated
from mesa.datacollection import DataCollector     #This output a Pandas file
from mesa.space import NetworkGrid        #This means the model runs on  network (high dimentional space)


def number_state(model, state):
    return sum([a.state == state for a in model.grid.get_all_cell_contents()])

#this masures the spread of fake news (fake point +1)
def number_infected_fake(model):   
    return number_state(model, 1)

#this masures the spread of real news (fake point -1)
def number_infected_real(model):
    return number_state(model, -1)

def infected_list(model):
    return model.datacollector.get_model_vars_dataframe()


class InfoSpread(Model):
    """A virus model with some number of agents"""

    def __init__(self, num_nodes=10, avg_node_degree=3, rewire_prob=.1, initial_outbreak_size=1, threshold_fake = 2, threshold_real = -2):
        self.num_nodes = num_nodes
        self.G = nx.watts_strogatz_graph(n=self.num_nodes, k= avg_node_degree, p=rewire_prob)   #G generate graph structure
        self.grid = NetworkGrid(self.G) #grid is the Masa native defintion of space: a coorindate with specified topology on which agents sits and interact
        self.schedule = SimultaneousActivation(self)
        self.initial_outbreak_size = (
            initial_outbreak_size if initial_outbreak_size <= num_nodes else num_nodes
        )

        self.datacollector = DataCollector(
            {
                "Infected_fake": number_infected_fake,
                "Infected_real": number_infected_real,
            }
        )

        # Create agents
        for i, node in enumerate(self.G.nodes()):
            a = User(
                i,
                self,
                0,  #make the state a int
                threshold_fake,
                threshold_real
            )
            self.schedule.add(a)
            # Add the agent to the node
            self.grid.place_agent(a, node)

        # Infect some nodes, initial infection bug free
        infected_nodes_fake = self.random.sample(self.G.nodes(), self.initial_outbreak_size)
        infected_nodes_real = self.random.sample(self.G.nodes(), self.initial_outbreak_size) 

        for a in self.grid.get_cell_list_contents(infected_nodes_fake):
            a.state = 1
            neighbors_nodes = self.grid.get_neighbors(a.pos)
            for n in self.grid.get_cell_list_contents(neighbors_nodes):
                n.state = 1
                
        for a in self.grid.get_cell_list_contents(infected_nodes_real):
            a.state = -1
            neighbors_nodes = self.grid.get_neighbors(a.pos)
            for n in self.grid.get_cell_list_contents(neighbors_nodes):
                n.state = -1  
                
        """
        state measures fake score!! the more negative the less likely to spread fake news
        also this model assumes that 
        1
        one piece of real news can cancel out one piece of fake news
        This model can be modulated by changing the value of fake and real
        
        2
        the inital braeakout size of fake and real news are the same
        This can be chaged by introducing a different initial breaksize for real and fake news
        however this score is kepet the same intentionally because too uch complexity is not good for modeling
        """        

        self.running = True
        self.datacollector.collect(self)

    def proportion_infected_fake(self):
        try:
            tot_fake = 0
            for i in self.grid.get_cell_list_contents(self.G):
                if i.state == 1:
                    tot_fake += 1
            return  tot_fake/ self.num_nodes
        except ZeroDivisionError:
            return math.inf
        
    def proportion_infected_real(self):
        try:
            tot_real = 0
            for i in self.grid.get_cell_list_contents(self.G):
                if i.state == -1:
                    tot_real += 1
            return  tot_real/ self.num_nodes
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
    def __init__(self, unique_id, model, initial_state, threshold_fake, threshold_real):
        super().__init__(unique_id, model)   #super(). is to inherent agent's property. The user class is a subset of the agent class with additional properties. All the papermeter here are inherited from orginial agent class, everything is new and specific to the user class
        self.state = initial_state
        self.threshold_fake = threshold_fake
        self.threshold_real = threshold_real


    def get_infected_neighbor_count(self):
        '''Count how many of neighbors are infected'''
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, include_center=False)
        influence_count = 0
        for n in self.model.grid.get_cell_list_contents(neighbors_nodes):
            influence_count += n.state
        return (influence_count)
        

    def step(self):
        '''Calculates what the state should be in the next step'''
        # Start as the current state and modify below
        self._next_state = self.state
        count = self.get_infected_neighbor_count()
        if count >= self.threshold_fake:
            self._next_state = 1
        elif count <= self.threshold_real:
            self._next_state = -1
            
    def advance(self):
        self.state = self._next_state
