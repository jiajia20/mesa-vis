#


import networkx as nx
from agent import *
from propagate import *

def batch_run(network_size = 100 ,average_neighbor=10,rewire=0.6, patient_zero_percentage=1, treshold_index=2):
    #####set-up the graph #######
    #make a graph
    ws = nx.watts_strogatz_graph(network_size, average_neighbor, rewire, seed=11)
    #initialize a network of agent
    ws_di = initialize_network_agent(ws)
    #initialize treshold
    for i in range(network_size): #network_size
        ws_di.get(i).change_tresh(treshold_index) #treshold_index

    #seed the rumor
    initialize_patient_zero(ws,ws_di, patient_zero_percentage) #patient_zero_percentage 
    
    ##### record numbers########
    # numbers
    infection = []
    suspect = []
    clean = []

    #initialize
    infection_num = 0
    sus_num = 0
    clean_num = 0

    #record first round
    for i in range (len(ws_di)):
        #see if neighbor infected
        neighbors = [n for n in ws.neighbors(i)]
        total_infected = 0
        for j in neighbors:
            if ws_di.get(j).infected == 1:
                total_infected += 1  
        if ws_di.get(i).infected == 1: # red
            infection_num += 1
        elif total_infected > 0: #yellow
            sus_num += 1   
    clean_num = len(ws_di) - infection_num - sus_num
    infection.append(infection_num)
    suspect.append(sus_num)
    clean.append(clean_num)
    
    #play and record second round -- I could have use anotehr function but really don't worth the effort
    step(ws,ws_di)
    #initialize
    infection_num = 0
    sus_num = 0
    clean_num = 0
    for i in range (len(ws_di)): #traverse whole graph to see situation of every node
        #see if neighbor infected
        neighbors = [n for n in ws.neighbors(i)]
        total_infected = 0
        for j in neighbors:
            if ws_di.get(j).infected == 1:
                total_infected += 1  
        if ws_di.get(i).infected == 1: # red
            infection_num += 1
        elif total_infected > 0: #yellow
            sus_num += 1     
    clean_num = len(ws_di) - infection_num - sus_num
    infection.append(infection_num)
    suspect.append(sus_num)
    clean.append(clean_num)
    
    while (infection[len(infection)-1] != infection[len(infection)-2]): #if the last two elements are not the same, keep looping
        step(ws,ws_di)
         #initialize
        infection_num = 0
        sus_num = 0
        clean_num = 0
        for i in range (len(ws_di)):
            #see if neighbor infected
            neighbors = [n for n in ws.neighbors(i)]
            total_infected = 0
            for j in neighbors:
                if ws_di.get(j).infected == 1:
                    total_infected += 1  
            if ws_di.get(i).infected == 1: # red
                infection_num += 1
            elif total_infected > 0: #yellow
                sus_num += 1
        clean_num = len(ws_di) - infection_num - sus_num
        infection.append(infection_num)
        suspect.append(sus_num)
        clean.append(clean_num)

    return(infection, suspect, clean)  
