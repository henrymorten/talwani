import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
import numpy as np
#random temp density value:
density = 450 #Kg/m3
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
    containing (x,z) coordinate pairs for the different vertice of the polygon in the subsurface.

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

def plotter(self):
    """
    """
    x_coords = self.points['x']
    y_coords = self.points['y']

    # Group the points as columns in a matrix
    P = np.vstack((x_coords, y_coords))

    # Calculate the centroid of the points
    c = np.mean(P, axis=1)

    # Calculate the vectors connecting points to the centroid
    d = P - np.expand_dims(c, axis=1)

    # Calculate angles of the vectors using atan2
    th = np.arctan2(d[1, :], d[0, :])

    # Sort angles and get corresponding indices
    si = np.argsort(th)
    st = th[si]

    # Rearrange the original points based on the sorted indices
    sP = P[:, si]

    # Add the first point again to close the polygon
    sP_closed = np.column_stack((sP, sP[:, 0]))

    Poly = Polygon(sP_closed.T,closed=True, edgecolor = 'black', facecolor='gray')

    #X coordinates to calculate G_v at:
    X_places = np.linspace(min(x_coords)-(0.5*max(x_coords)),max(x_coords)+(0.5*max(x_coords)),100*len(x_coords) )

    # plot
    self.ax1.clear()  # Clear previous plot
    self.ax1.plot(X_places, talwani(X_places, polygon_cords=sP_closed, density=density))
    self.ax1.figure.canvas.draw()

class DraggablePoint:
    def __init__(self, ax, point, points_list):
        self.ax = ax
        self.point = point
        self.points_list = points_list
        self.press = None
        self.cid_press = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.ax:
            return
        if self.point.contains(event)[0]:
            self.press = (self.point.center, event.xdata, event.ydata)
        else:
            self.press = None

    def on_motion(self, event):
        if self.press is None:
            return
        if event.inaxes != self.ax:
            return
        previous_center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        new_center = (previous_center[0] + dx, previous_center[1] + dy)
        self.point.set_center(new_center)
        self.point.figure.canvas.draw()

    def on_release(self, event):
        if self.press is not None:
            # Update the points list with the new coordinates
            index = [i for i, point in enumerate(self.points_list['x']) if point == self.press[0][0]]
            if index:
                index = index[0]
                self.points_list['x'][index] = self.point.center[0]
                self.points_list['y'][index] = self.point.center[1]
            self.press = None
            if len(self.points['x']) >= 3 and len(self.point['y']) >= 3:
                # Extract x and y coordinates
                plotter(self)

class PointMarker:
    def __init__(self, xlim, ylim):
        # Create subplots with a grid of 2 rows and 1 column, both rows have equal width
        self.fig, (self.ax1, self.ax) = plt.subplots(nrows=2, ncols=1,)
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        #self.ax.set_aspect('equal')
        self.points = {'x': [], 'y': []}
        self.markers = []  # List to store draggable markers
        self.cid_left = self.fig.canvas.mpl_connect('button_press_event', self.on_left_click)
        self.cid_right = self.fig.canvas.mpl_connect('button_press_event', self.on_right_click)
        self.points_to_save = None

    def on_left_click(self, event):
        if event.inaxes and event.button == 1:  # Check for left mouse button (button == 1)
            x, y = event.xdata, event.ydata
            clicked_existing_point = False
        
            if len(self.points['x']) >=3 and len(self.points['y']) >= 3:
                # Extract x and y coordinates
                plotter(self)


            # Check if an existing point is clicked
            for marker in self.markers:
                contains, _ = marker.point.contains(event)
                if contains:
                    clicked_existing_point = True
                    break

            if not clicked_existing_point:
                self.points['x'].append(x)
                self.points['y'].append(y)
                marker = Circle((x, y), 0.2, color='red', picker=True)  # Red circle marker
                self.ax.add_patch(marker)
                self.markers.append(DraggablePoint(self.ax, marker, self.points))

            self.fig.canvas.draw()

    def on_right_click(self, event):
        if event.inaxes and event.button == 3:  # Check for right mouse button (button == 3)
            self.points_to_save = dict(self.points)  # Save the marked points
            plt.close(self.fig)  # Close the plot

    def show_plot(self):
        plt.show()

if __name__ == "__main__":
    xlim = (0, 20)  # Set your desired x-axis limits
    ylim = (0, 20)  # Set your desired y-axis limits
    marker = PointMarker(xlim, ylim)
    marker.show_plot()

    # Access the saved points after the plot is closed
    saved_points = marker.points_to_save
    print("Saved Points:", saved_points)






