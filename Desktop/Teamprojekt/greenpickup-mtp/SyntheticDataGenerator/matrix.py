import numpy as np
import random
import math
import numpy as np
import matplotlib.pyplot as plt

def get_color(value):
    # Define gradient colors
    darkblue = (0, 0, 139)
    lightred = (255, 99, 71)
    # Calculate color value based on position in gradient
    fraction = value / 100.0
    r = int(darkblue[0] + fraction * (lightred[0] - darkblue[0]))
    g = int(darkblue[1] + fraction * (lightred[1] - darkblue[1]))
    b = int(darkblue[2] + fraction * (lightred[2] - darkblue[2]))
    return (r, g, b)

class Matrix:
    def __init__(self):
        print("Matrix class has been loaded.")

    def generateMatrix(north, south, east, west):
        #north, south, east, west = 48.8663994, 48.6920188, 9.3160228, 9.0386007

        min_lat, max_lat, min_lon, max_lon = south, north, west, east
        resolution = 0.001  # 1,000 meters in decimal degrees, approximate value
        # Create the matrix
        rows = int((max_lat - min_lat) / resolution)
        cols = int((max_lon - min_lon) / resolution)
        matrix = np.zeros((rows, cols), dtype=int)
        return matrix
    
    def incrementMatrix(coordinates, north, south, east, west, matrix):
        resolution = 0.001
        for i in range(len(coordinates)):
            '''
            x = round((coordinates[i][1] - west) / ((east - west)))
            print(str((coordinates[i][1] - west) / ((east - west))))  
            y = round((coordinates[i][0] - south) / ((north - south)))
            print(str((coordinates[i][0] - south) / ((north - south))))
            '''
            
            dx=(east-west)/len(matrix[0])
            dy=(north-south)/len(matrix)

            x = round((coordinates[i][0] - south) / dx)
            y = round((coordinates[i][1] - west) / dy)
            matrix[x][y] = matrix[x][y] + 1
            print("Cell: " + str(x) + "/" + str(y) + " has been incremented to: " + str(matrix[x][y]))
        return matrix

    def plotMatrix(matrix):
        # Normalize the matrix so the maximum value is 1
        matrix_norm = matrix / np.max(matrix)

        # Create a colormap from dark blue to bright red
        cmap = plt.get_cmap('RdYlBu_r')

        # Plot the matrix as an image with the colormap
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(matrix_norm, cmap=cmap)
        plt.show()
        '''
        # Print matrix as grid with colored cells
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                # Calculate color based on value
                value = matrix[i][j]
                color = get_color(value)
                # Print cell with value and colored background
                print(f"\x1b[48;2;{color[0]};{color[1]};{color[2]}m {value:^3} \x1b[0m", end="")
            print()
        '''


'''


# Generate a random matrix with values between 0 and 1
matrix = np.random.rand(174, 277)

# Normalize the matrix so the maximum value is 1
matrix_norm = matrix / np.max(matrix)

# Create a colormap from dark blue to bright red
cmap = plt.get_cmap('RdYlBu_r')

# Plot the matrix as an image with the colormap
fig, ax = plt.subplots(figsize=(10, 6))
ax.imshow(matrix_norm, cmap=cmap)
plt.show()
'''