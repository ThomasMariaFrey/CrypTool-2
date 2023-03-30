"""routePlanning

This module is used to plan the routes between the given pick up locations.

"""

from multiprocessing import Process
import osmnx as ox
import networkx as nx
import pandas as pd

class RoutePlanning():
    '''
    Plans the route by the given pick up location for the given city.

    Parameters
    __________
    place_name: Place name
        The name of the place for that the routes are being planned
    routes: Pick up locations
        The locations between which the routes are being planned
    
    '''
    def __init__(self):
        '''
        Initializes the route planning module

        Parameters
        __________
        place_name: Place name
            The name of the place for that the routes are being planned
        routes: Pick up locations
            The locations between which the routes are being planned
    
        '''
        print("Route Planning class has been loaded.")

    def plan_route(place_name,dataframe, north, south, east, west):
        '''
        Process that plans the routes between pick up locations in a place and creates the map.

        Parameters
        __________
        place_name: Place name
            The name of the place for that the routes are being created.
        dataframe: Pick-up locations
            The pick up locations between which the routes are being planned
        '''

        grouped = dataframe.groupby('cluster')
        dfs = {}
        for group_name, group_df in grouped:
            dfs[group_name] = group_df
        list_of_coordinate_lists = []
        for group_name, group_df in dfs.items():
            print(f"{group_name} DataFrame:")
            group_df = group_df.drop("cluster",axis=1)
            print(group_df)
            list_of_coordinate_lists.append(list(zip(group_df['x'],group_df['y'])))
        #Appending the first list to the end of the list of lists. This is to ensure a full circle.
        list_of_coordinate_lists.append(list(zip(dfs[0]['x'],dfs[0]['y'])))
        # Display the result
        print(list_of_coordinate_lists)


       

           
   
        #G = ox.graph_from_place(place_name, network_type='drive')
        G = ox.graph_from_bbox(north, south, east, west, network_type='drive')
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        routes = [] 

        list_of_nearest_nodes_lists = []
        for i in range((len(list_of_coordinate_lists)-1)):
            list_of_nearest_nodes = []
            for j in range((len(list_of_coordinate_lists[0]))):#-1 here before
                #Snapping the coordinates to the nearest node in the graph
                try:
                    graph = ox.graph_from_point(list_of_coordinate_lists[i][j], dist=1000, network_type='drive') #5000 befor
                except Exception as e:
                    print("Expception!")
                    print(e)
                    pass
                nearest_node = ox.distance.nearest_nodes(graph, list_of_coordinate_lists[i][j][0], list_of_coordinate_lists[i][j][1])
                list_of_nearest_nodes.append(nearest_node)
                print("i: " + str(i) + " j: " + str(j))
                print(nearest_node)
            list_of_nearest_nodes_lists.append(list_of_nearest_nodes)
        print(list_of_nearest_nodes_lists)


        nodes_pos_list = []
        nodes_coords_list = []
        edges_list = []
        for i in range((len(list_of_nearest_nodes_lists)-1)):
            for j in range((len(list_of_nearest_nodes_lists[0]))):

                try:
                    route = nx.shortest_path(G, list_of_nearest_nodes_lists[i][j], list_of_nearest_nodes_lists[i+1][j])
                    print("i: " + str(i) + " j: " + str(j))
                    print(route)
                    routes.append(route)
                    
                    #node_pos = nx.get_node_attributes(G, 'pos')
                    #nodes_pos_list.append(node_pos)
                    #node_coords = [node_pos[node] for node in route]
                    #nodes_coords_list.append(node_coords)
                    edges = list(zip(route[:-1], route[1:]))
                    edges_list.append(edges)

                    

                except Exception as e:
                    print("Expception!")
                    print(e)
                    pass

        #print(nodes_pos_list)
        #print(nodes_coords_list)
        print(edges_list)
        nodes = list(G.nodes())
        '''
        for edge in edges:
            start_node_lat, start_node_lon = G.nodes[edge[0]]['y'], G.nodes[edge[0]]['x']
            end_node_lat, end_node_lon = G.nodes[edge[1]]['y'], G.nodes[edge[1]]['x']
        print(start_node_lat)
        print(start_node_lon)
        print(end_node_lat)
        print(end_node_lon)
        '''
        #fig, ax = ox.plot_graph_routes(G, routes, node_size=0, route_alpha=0.1)

        return(edges_list)



'''
                route = nx.shortest_path(G, list_of_coordinate_lists[i][j], list_of_coordinate_lists[i][j+1])
                print("i: " + str(i) + " j: " + str(j))
                print(route)
                routes.append(route)
        fig, ax = ox.plot_graph_routes(G, routes, node_size=0)
'''
