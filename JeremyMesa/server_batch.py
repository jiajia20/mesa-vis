import math

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import ChartModule
from mesa.visualization.modules import TextElement
from .model import InfoSpread, number_infected

# from mesa.visualization.modules import NetworkModule
# from .batchrun import batch_run
#This visualization won't include network visualization but instead will only focus on visualing batch run data






#input module

#The elements are added to the visualization in the order they appear, so the chart will appear underneath the grid.








#Consolidating the batch run file because 

from mesa.batchrunner import BatchRunner
from .model import model """ something else??"""
from mesa.datacollection import DataCollector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Find the time it needed to infect the whole/part network
def find_last_increase (a):
    i = 0
    for i in range(len(a)-2):
        if a[i] != a[i+1]:
            i += 1
        else:
            return(i+1)
    return(i+1)

def calculate_infection_time(df):
    time = []
    for i in range(df.shape[0]):
        inf_data = df['infection_list'][i]['Infected'].values.tolist()
        infection_time = find_last_increase(inf_data)
        time.append(infection_time)
    return(time)

#calculate percentage of infection
def find__final_infection_number (a):
    i = 0
    for i in range(len(a)-2):
        if a[i] != a[i+1]:
            i += 1
        else:
            return(a[i+1])
    return(a[i+1])

def calculate_total_infection(df):
    total_inf = []
    for i in range(df.shape[0]):
        inf_data = df['infection_list'][i]['Infected'].values.tolist()
        infection_num = find__final_infection_number(inf_data)
        total_inf.append(infection_num)
    return(total_inf)




#regular batch runner input
fixed_params = {"avg_node_degree":10,
                "num_nodes": 400,
               "initial_outbreak_size" : 1,
                "threshold" : 3
                }
variable_params = {
                      "rewire_prob": [0.000001, 0.00001,0.0001,0.001,0.01,0.1,1]
                  }  #  {"rewire_prob": range(0.05, 1.0, 0.05)}

batch_run = BatchRunner(InfoSpread,
                        variable_params,
                        fixed_params,
                        iterations=1,
                        max_steps=100,
                        model_reporters={"infection_list": infected_list})

#Batch runner GUI set up 
if __name__ == '__main__':
    # running the full iteration of model: round = variable parameter x rounds of iteration
    batch_run.run_all() 
    
    # getting the pandas data frame
    run_data = batch_run.get_model_vars_dataframe()
    
    #data processing
    #This instance shows only the 
    x = run_data.rewire_prob
    time = calculate_infection_time(run_data)
    plt.plot(x,time,'o', color = '#3CAEA3', alpha = 0.3)
    plt.xlabel("rewiring probability")
    plt.ylabel("steps to infect network")
    plt.title("400 agents, 10 avergae neighbors, 3 treshold")
    plt.xticks(x)
    plt.xscale('log')
    plt.show()
    
