#propage: check if neighbors infect - random chance of infection
#I see, the problem is that this proprage the whole network, instead of spreading it in steps  

def step(network, directory):
    #first create a dictionary of number of infection
    infection_dic = {}
    for i in range(len(directory)):
        agent = directory.get(i)
        neighbors = [n for n in network.neighbors(i)]
        total_infected = 0
        for j in neighbors:
            if directory.get(j).infected == 1:
                total_infected += 1
        infection_dic.update({i:total_infected})
       
    #update all at once
    for i in range(len(directory)):
        if infection_dic.get(i) >= directory.get(i).infect_treshold:
            directory.get(i).infect()
    
    return
    #debug step: print whoever that's infected   