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

#batch running test 2
from mesa.batchrunner import BatchRunner

#num_nodes=10, avg_node_degree=3, rewire_prob=.1, initial_outbreak_size=1, threshold = 2
rewire_list = []
for i in range(21):
    rewire_list.append(round((i*0.05),3))
#rewire_list = [0, 0.1, 0.2, 0.3]

fixed_params = {"num_nodes": 80,
               "avg_node_degree": 8,
               "initial_outbreak_size" : 1,
               "threshold" : 2}
variable_params = {"rewire_prob": rewire_list}  #  {"rewire_prob": drange(0.05, 1.0, 0.05)}

batch_run = BatchRunner(InfoSpread,
                        variable_params,
                        fixed_params,
                        iterations=5,
                        max_steps=10,
                        model_reporters={"infection_list": infected_list})
batch_run.run_all()