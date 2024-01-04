import random
import numpy as np


#random temp density value:
G=6.67e-11 #NM2/kg3
SI2mGAL = 1e5

def talwani(xp, polygon_cords, density):
    """
    This function calculates the vertical gravitational attraction (g_z) of a 2D subsurface body using the formula of Talwani et al. (1959).
    Can be accessed here: https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/JZ064i001p00049 (as of 03/10/23).

    Note that all input units are in SI, and the output of the function (gravitational attraction) is in mGal. 
    the coordinate system relies on +Z == -Y (DOWN)

    ------------------------------------------------------
    Input parameters: 

    xp: numpy array
    points along the x - axis (distance along the profile) at which points to calculate the vertical gravitational attraction at each of the corresponding points.

    polygon_cords: numpy array
    containing (x,z) coordinate pairs for   different vertice of the polygon in the subsurface.

    desnity: float
    desnsity of the rock in the subsurface

    ------------------------------------------------------
    Output parameter:
    g_z: array 
    the calculated vertical component of the gravitrational attraction at each x coordinate in xp. 
    
    ------------------------------------------------------
    Refrences:

    Talwani, M., J. L. Worzel, and M. Landisman (1959), Rapid Gravity Computations
    for Two-Dimensional Bodies with Application to the Mendocino Submarine
    Fracture Zone, J. Geophys. Res., 64(1), 49-59, doi:10.1029/JZ064i001p00049.

    Uieda, L., V. C. Oliveira Jr, and V. C. F. Barbosa (2013), Modeling the Earth with Fatiando a Terra, Proceedings of the 12th Python in Science Conference, pp. 91-98. doi:10.25080/Majora-8b375195-010

    """
    #x and 'y' (-y -> + z) coordinates of the polygon 
    x = polygon_cords[0,:]
    z = polygon_cords[1,:]

    #Define this as 0 as all measuremrents are taken from Z=0 (assumed to be on the surface of the earth)
    zp = np.zeros(len(xp))

    #Final array to determine the total vertical acceleration due to gravity at every point
    final = np.zeros(len(xp))

    #Iterate over every vertice (Number of polygon coords - 1)
    for v in range(len(x)-1):
        xv = x[v] - xp
        zv = z[v] - zp 

        if v == len(x) - 1:
            #Denoting xv_(i+1) etc
            xvp1 = x[0] - xp
            zvp1 = z[0] - zp 

            #The last verice pairs with the first one
        else:
            xvp1 = x[v + 1] - xp
            zvp1 = z[v + 1] - zp

        #Fix to deal with the extremal limits that don't really work. Inspiration for this code has beenm taken heavily from the Fatiando team: 
        #https://www.fatiando.org/index.html
        # or more specifically: https://programtalk.com/vs2/python/4196/fatiando/fatiando/gravmag/talwani.py/

        #I spent absolutely ages trying to get all of the extremal limits to work as outlined by (Talwani et al., 1959) and lets just be happy with the temporary fix as outlined below instead. Just add 0.01 to everything to make sure theres no /0 errors etc. 

        xv[xv == 0.] += 0.01
        xv[xv == xvp1] += 0.01

        zv[zv[xv == zv] == 0.] += 0.01
        zv[zv == zvp1] += 0.01

        zvp1[zvp1[xvp1 == zvp1] == 0.] += 0.01
        xvp1[xvp1 == 0.] += 0.01
        #End of the fix (some may call it a bodge)

        phi = np.arctan2(zvp1 - zv,xvp1 - xv)
        a = xvp1 + zvp1 * (xvp1 - xv) / (zv - zvp1)
        theta = np.arctan2(zv, xv)
        theta_p1 = np.arctan2(zvp1, xvp1)
        theta[theta < 0] += np.pi
        theta_p1[theta_p1 < 0] += np.pi

        temp = a * np.sin(phi) * np.cos(phi) * (
                theta - theta_p1 + np.tan(phi) * np.log(
                    (np.cos(theta) * (np.tan(theta) - np.tan(phi))) /
                    (np.cos(theta_p1) * (np.tan(theta_p1) - np.tan(phi)))
                    )
                )
    
        temp[theta == theta_p1] = 0.
        final = final + temp

    g_z = 2*G*final*density*SI2mGAL

    return g_z


