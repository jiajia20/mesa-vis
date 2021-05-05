class agent:
    def __init__(self,i):
        self.infected = 0 #network started with no one beliving a specific peice of info, 
        self.index = i #to keep track of 
        self.infect_treshold = 2 #should be a integer
    
        
    def infect(self):
        self.infected = 1
    
    def change_tresh(self, infect_treshold_i):
        self.infect_treshold = infect_treshold_i


import random 

def initialize_network_agent(network):
    directory = {} 
    node_num = network.number_of_nodes()
    for i in range (node_num):
        directory.update({i:agent(i)})
    return directory

#change trashold
def change_all_tresh(directory,new_tresh_list):
    for i in range(len(directory)):
        agent = directory.get(i)
        agent.change_tresh(new_tresh_list[i])


#choose a random neighborhood to infect

def initialize_patient_zero(network, directory, percentage=1):
    x = random.randint(1,len(directory)-1) ##something wrong here but I haven't fix
    patient_zero = directory.get(x)
    patient_zero.infect()
    
    #randomly infect a portion of patient zero's network
    neighbors = [n for n in network.neighbors(x)]
  
    for i in neighbors:
        dice = random.random()
        if dice < percentage:
            patient_one = directory.get(i)
            patient_one.infect()
    return x