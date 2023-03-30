"""clusteringAlgorithm

This module is used to calculate the centroids of movement streams and to return them for further
usage by the clustering prototype.

"""
from multiprocessing import Process
import random
import osmnx as ox
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
import pandas as pd


class CreateCoordinates:
    '''
    Clusters the provided movement data and does the required calculations for this.

    Parameters
    __________
    place_name: Place name
        The name of the place for which the historic movement data is being clustered.
    
    '''
    def __init__(self):
        '''
        Initializes the clustering algorithm
    
        '''
        print("Clustering algorithm class has been loaded.")
    
    def create_datapoints(north, south, east, west, boundary_points):
        '''
        Populates the map with synthetic data

        Returns
        _______
        coordinates: The list of centroids of the middlepoints of the generated synthetic data.
        '''
        # debug
        #This is the amount of clusters that will be created on the map. Please note that 
        #one further cluster will be added in the center of the city of stuttgart
        clusters = 9
        #clusters = int(input("Please enter the amount of clusters."))
        # debug
        #The amount of data points that are associated with every cluster. The amount of routes are
        #The amount of clusters times the amount of data points
        datapoints = 500
        #datapoints = int(input("Please enter the amount of datapoints for each of the " + str(clusters) + " clusters."))
        
        xMin,yMin,xMax,yMax = west, south, east, north
        # Generate random centers for the clusters, evenly distributed within the square

        x_range = (xMax - xMin) * 0.25
        y_range = (yMax - yMin) * 0.25

        x_midpoint = (xMax + xMin) * 0.5
        y_midpoint = (yMax + yMin) * 0.5

        x_centers = [random.uniform(x_midpoint - x_range, x_midpoint + x_range)
                     for i in range(clusters)]
        y_centers = [random.uniform(y_midpoint - y_range, y_midpoint + y_range)
                     for i in range(clusters)]


        centers = [(x_centers[i], y_centers[i]) for i in range(clusters)]
        centers.append((9.1681,48.7752))

        # Create an empty list to store the points
        points = []
        
        # Calculate pairwise distances between points
        distances = distance.cdist(boundary_points, boundary_points)

        # Calculate the average distance
        avg_distance = np.mean(distances)

        # Create three clusters of 10 points each
        for cluster in range(clusters+1):
            # Generate 10 random points within a small radius of the cluster center
            for i in range(datapoints):
                #The number 6 has been chosen absolutely random
                x_offset = random.uniform((-avg_distance/6), (avg_distance/6))
                y_offset = random.uniform((-avg_distance/6), (avg_distance/6))
                x_center, y_center = centers[cluster]
                x = x_center + x_offset
                y = y_center + y_offset
                # Add the point and its cluster number to the list
                points.append((x, y, cluster))
        #Create a dataframe from the list of points
        #For some reason this is the wrong way around
        dataframe = pd.DataFrame(points, columns=['y', 'x', 'cluster'])
        return dataframe

    def generate_boundary_points(place_name):
        '''
        Generates the boundary points around the given place

        Returns
        __________
        boundary_points: Boundary points
            A list of points forming a boundary around the given place. This is used for further 
            calculations of this software artifact.
    
        '''
        print("Generating boundary points...")
        print("Calculating GPS outline of " + place_name + "...")
        city_boundary = ox.geocode_to_gdf(place_name)

        # extract the first polygon in the GeoDataFrame and get its exterior coordinates
        boundary_coords = city_boundary.iloc[0]["geometry"].exterior.coords[:]

        # convert the coordinates to a list of points
        boundary_points = [(lat, lon) for lon, lat in boundary_coords]
        return boundary_points


def get_extremes(points):
    '''
    Gets the extremes of a list of points

    Parameters
    __________
    points: Points
        List of points from that the extremes are being chosen.

    Returns
    _______
    lowest_x, lowest_y, highest_x, highest_y: The lowest and highest x values of the list of points
    that were given to the method as parameters.
    
    '''
    lowest_x = highest_x = points[0][0]
    lowest_y = highest_y = points[0][1]
    for point in points:
        x, y = point
        if x < lowest_x:
            lowest_x = x
        elif x > highest_x:
            highest_x = x
        if y < lowest_y:
            lowest_y = y
        elif y > highest_y:
            highest_y = y
    return lowest_x, lowest_y, highest_x, highest_y