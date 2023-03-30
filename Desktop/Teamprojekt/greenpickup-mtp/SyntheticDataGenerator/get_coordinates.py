import numpy as np
import osmnx as ox
import networkx as nx

class GetCoordinates:
    def __init__(self):
        print("getCoordinates class has been loaded.")

    def getCoordinates(data_list, north, south, east, west):
        print("getting the coordinates")
        
        #edges_list = list(G.edges(data=True))
        coordinate_list = []
        '''
        for i in range(len(coordinate_list)):
            start_node_lat = edges_list[data_list[i]]['y']
            start_node_lon = edges_list[data_list[i]]['x']
            #end_node_lat = end_node_id[data_list[i]]['y']
            #end_node_lon = end_node_id[data_list[i]]['x']
            starttuple = (start_node_lat,start_node_lon)
            #endtuple = (end_node_lat,end_node_lon)
            coordinate_list.append(starttuple)
            #coordinate_list.append(endtuple)
            print(str(i))
            print(str(coordinate_list[i]) + ": " + str(starttuple))
        '''
        print(data_list)
        G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
        nodes = list(G.nodes())
        for i in range(len(data_list)):
            for edge in data_list[i]:
                #try:
                start_node_lat, start_node_lon = G.nodes[edge[0]]['y'], G.nodes[edge[0]]['x']
                end_node_lat, end_node_lon = G.nodes[edge[1]]['y'], G.nodes[edge[1]]['x']
                starttuple = (start_node_lat,start_node_lon)
                endtuple = (end_node_lat,end_node_lon)
                coordinate_list.append(starttuple)
                coordinate_list.append(endtuple)
                print(str(starttuple) + "/" + str(endtuple))
                #except Exception as e:
                #    print("Exception for " + str(edge) + "!")
                #    print(e)
                #    pass

        return coordinate_list




