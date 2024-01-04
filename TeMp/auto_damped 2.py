import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import talwani

profile = pd.read_csv('test_profile.csv',delimiter=',',header=None)

test_coords = np.array([
    [1, 0.623, 0.222, 0.9, 0.9, 0.222, 0.623],  # X Coordinates
    [-0.45, -0.782, -0.975, -0.225, -0.225, -0.975, -0.782]  # Y Coordinates
])*100

def pnts2poly(points):
    """
    Takes random coordinates and converts them to a coherant polygon. 
    Assumes that: [0,:] are the X coordinates.
    and that [1,:] are the y coordinates for the indervidual coordinates. 
    assumes coordinates with be provided in the shape (2xN).
    """
    c = np.mean(points, axis=1)

    # Calculate the vectors connecting points to the centroid
    d = points - np.expand_dims(c, axis=1)

    # Calculate angles of the vectors using atan2
    th = np.arctan2(d[1, :], d[0, :])

    # Sort angles and get corresponding indices
    si = np.argsort(th)
    st = th[si]

    # Rearrange the original points based on the sorted indices
    sP = points[:, si]

    # Add the first point again to close the polygon
    sP_closed = np.column_stack((sP, sP[:, 0]))
    
    return sP_closed

def dist_to_mid(coords):
    """
    Takes in cartesian coordinates for a polygon - and calculates the appropriate polar coordinates 
    in relation to the midpoint of the Polygon.
    """
    midpoint = np.mean(coords, axis= 1) #Midpoint value as to base the polar coordinate system
    dx, dy = coords[0,:] - midpoint[0], coords[1,:] - midpoint[1] #calculates the change in distace from the polygon coordinates 
    #to the calculated midpoint of the polygon. 

    r = np.sqrt(dx**2 + dy**2) #works out the distance from the midpoint to the polygon coordinates 
   
    return np.array([coords[0,:], coords[1,:], r])

def make_jacobian(xp, polygon_cords, density):
    """
    Calculate the Jacobian matrix for the talwani function.

    Parameters:
    xp: numpy array
        Points along the x-axis.
    polygon_cords: numpy array
        Coordinates of the polygon vertices.
    density: float
        Density of the rock.

    Returns:
    Jacobian_matrix: numpy array
        Jacobian matrix.
    """

    jacobian = np.empty((len(xp), len(xp)))
    print(jacobian.shape)
    print("")
    #Calculate base gravitational attraction
    gz_base = talwani.talwani(xp, polygon_cords, density)
    
    #Delta for the finite differences
    delta = 1e-6

    #Add the small pertubation to all of the variable paramaters 
    gz_per = talwani.talwani(xp+delta, polygon_cords, density)

    fin_diff = (
        (
        gz_per - gz_base
        ) / delta
    )
    print(fin_diff.T.shape)
    print("")
    print(jacobian)
    print("")
    print(fin_diff)
    print("")
    print(np.eye(len(xp)))
    print("")

    print(np.eye(len(xp))@ fin_diff.reshape((len(xp),1)))
    return 


#Defining coordinates to model within
#These are in SI Base units, M
xmin = min(profile[0])
xmax = max(profile[0]*1000)
ymin = 0
ymax = 20_000
density = 450  # Kg/m3
G = 6.67e-11  # NM2/kg3
SI2mGAL = 1e5
npoints = 3 # number of points I want the model to solve for.
xp = np.linspace(xmin, xmax, int(np.round(xmax, 0)))
coords = pnts2poly(test_coords)

print(make_jacobian(xp,coords, density))
