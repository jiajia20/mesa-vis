import networkx as nx
def vis(model):
    inf_count = []
    state_color = []
    for i in model.grid.get_cell_list_contents(model.G):
        inf_count.append(i.get_infected_neighbor_count())
        state = i.state
        if state == 1:
            state_color.append('#ED553B') # red
        elif state == -1:
            state_color.append('#3CAEA3') # green
        else:
            state_color.append('#F6D55C') #yellow       
            
    inf_dic =  {}
    for i in range(model.num_nodes):
        inf_dic.update({i:(str(i),inf_count[i])})

    return(nx.draw_kamada_kawai(model.G, node_size=300,node_color=state_color, labels=inf_dic, alpha = 0.8))
    