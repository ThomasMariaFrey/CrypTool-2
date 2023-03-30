
from route_planning import RoutePlanning
from matrix import Matrix
from create_coordinates import CreateCoordinates
from get_coordinates import GetCoordinates
import numpy as np
import sys
import osmnx as ox
import networkx as nx

class Main:
    '''
    Initializes and runs the syntheticDataGenerator class

    Parameters
    __________
    The main class has no parameters
    
    '''
    def __init__(self):
        '''
        Initializes the syntheticDataGenerator.
    
        '''
        self.matrix = Matrix()
        self.createCoordinates = CreateCoordinates()
        self.routePlanning = RoutePlanning()

        G = ox.graph_from_bbox(48.8663994, 48.6920188, 9.3160228, 9.0386007, network_type='drive')
        '''
        #edge_list = list(G.edges(data=True))
        nodes = list(G.nodes(data=True))
        start_node_lat = G.nodes['130582629']['y']
        start_node_lon = G.nodes['130144342']['x']
        starttuple = (start_node_lat,start_node_lon)
        print(starttuple)

        x = input(...)
        '''

        ### V This one works V ###
        '''
        # loop through each edge and print the GPS data of its nodes
        G = ox.graph_from_bbox(48.8663994, 48.6920188, 9.3160228, 9.0386007, network_type='drive')
        edges = [(254861987, 59660004), (59660004, 527916243)]
        nodes = list(G.nodes())
        for edge in edges:
            start_node_lat, start_node_lon = G.nodes[edge[0]]['y'], G.nodes[edge[0]]['x']
            end_node_lat, end_node_lon = G.nodes[edge[1]]['y'], G.nodes[edge[1]]['x']
            print(str(start_node_lat) + " " + str(start_node_lon))
            print(str(end_node_lat) + " " + str(end_node_lon))
        '''
        

    def run(self):
        '''
        Runs the syntheticDataGenerator
    
        '''
        new_matrix = Matrix.generateMatrix(48.8663994, 48.6920188, 9.3160228, 9.0386007)
        print(new_matrix)
        print(new_matrix.shape)

        boundaryPoints = CreateCoordinates.generate_boundary_points('Stuttgart, Germany')

        newCoordinates = CreateCoordinates.create_datapoints(48.8663994, 48.6920188, 9.3160228, 9.0386007, boundaryPoints)
        print(newCoordinates)
        print(newCoordinates.shape)

        edgesList = RoutePlanning.plan_route('Stuttgart, Germany', newCoordinates, 48.8663994, 48.6920188, 9.3160228, 9.0386007)

        
        coordinate_list = GetCoordinates.getCoordinates(edgesList, 48.8663994, 48.6920188, 9.3160228, 9.0386007)

        new_matrix = Matrix.incrementMatrix(coordinate_list, 48.8663994, 48.6920188, 9.3160228, 9.0386007, new_matrix)

        np.set_printoptions(threshold=sys.maxsize)

        np.savetxt('new_matrix5000.txt',new_matrix,fmt='%.2f')
        new_matrix.astype('int16').tofile("new_matrixBit5000")
        print(new_matrix)
        Matrix.plotMatrix(new_matrix)



        

if __name__ == "__main__":
    main = Main()
    main.run()
    
