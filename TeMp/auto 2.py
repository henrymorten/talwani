import pandas as pd 
import numpy as np
from matplotlib.patches import Polygon
from scipy.interpolate import UnivariateSpline
from scipy.optimize import differential_evolution, dual_annealing, direct
import matplotlib.pyplot as plt
import talwani

profile = pd.read_csv('test_profile.csv',delimiter=',',header=None)
#profile = pd.read_csv('Iom1.csv',delimiter=',',header=None)

def objective(coords):
    coords = coords.reshape((2, npoints),order ='F')
    result = talwani.talwani(xp, pnts2poly(coords), density)
    print(f'Objective: {(np.sum(np.abs(np.abs(result) -np.abs(y_fine))))}')
    return np.sum(np.abs(np.abs(result) -np.abs(y_fine)))

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

#Run a spline curve through the data to allow direct comparison between the profile and the modelled gravity.
spline = UnivariateSpline(profile[0]*1000, profile[1])
x_fine = np.linspace(xmin, xmax, int(np.round(xmax, 0)))
y_fine = spline(x_fine)

#optimal = minimize(objective, in_guess,method='L-BFGS-B').x
#This minimize() func only finds a local minimum :(), not a global minimum

optimal = differential_evolution(
                                objective,
                                bounds= [(xmin,xmax),(-ymax,ymin)]*npoints,
                                ).x

optimal_coords = pnts2poly(optimal.reshape((2, npoints),order='F'))

optimized_result = talwani.talwani(xp,optimal_coords, density) 

Poly = Polygon(optimal_coords.T,closed=True, edgecolor = 'black', facecolor='gray')

plt.figure()
plt.subplot(211)
plt.plot(profile[0]*1000,profile[1],label="Profile")
plt.plot(xp, optimized_result,label="optimal")
#plt.plot(xp, y_fine,label="spline")
plt.legend()
plt.xlabel("Distance (m)")
plt.ylabel("Gravity (mGal)")

plt.subplot(212)
plt.gca().add_patch(Poly)
plt.scatter(optimal_coords[0], optimal_coords[1])
plt.xlim([0,xmax])
plt.ylabel("Depth (m)")
plt.xlabel("Distance (m)")
plt.tight_layout()
plt.show()
