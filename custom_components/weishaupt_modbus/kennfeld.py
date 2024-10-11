#from scipy.interpolate import CubicSpline
from numpy.polynomial import Chebyshev
import numpy as np

#import matplotlib.pyplot as plt

class PowerMap():
    # these are values extracted from the characteristic curves of heating power found ion the documentation of my heat pump.
    # there are two diagrams: 
    #  - heating power vs. outside temperature @ 35 °C flow temperature
    #  - heating power vs. outside temperature @ 55 °C flow temperature
    known_x = [   -30,   -25,   -22,   -20,   -15,   -10,    -5,     0,     5,    10,    15,    20,    25,    30,    35,    40]
    # known power values read out from the graphs plotted in documentation. Only 35 °C and 55 °C available
    known_y = [[ 5700,  5700,  5700,  5700,  6290,  7580,  8660,  9625, 10300, 10580, 10750, 10790, 10830, 11000, 11000, 11000 ],
               [ 5700,  5700,  5700,  5700,  6860,  7300,  8150,  9500, 10300, 10580, 10750, 10790, 10830, 11000, 11000, 11000 ]]

    # the known x values for linear interpolation
    known_t = [35, 55]

    # the aim is generating a 2D power map that gives back the actual power for a certain flow temperature and a given outside temperature
    # the map should have values on every integer temperature point
    # at first, all flow temoperatures are lineary interpolated 
    steps = 21
    r_to_interpolate = np.linspace(35, 55, steps)

    # the output matrix
    max_power = []

    interp_y = []

    def __init__(self) -> None:
        # build the matrix with linear interpolated samples
        # 1st and last row are populated by known values from diagrem, the rest is zero
        self.interp_y.append(self.known_y[0])
        v = np.linspace(0, self.steps-3, self.steps-2)
        for idx in v:
            self.interp_y.append(np.zeros_like(self.known_x))
        self.interp_y.append(self.known_y[1])

        for idx in range(0, len(self.known_x)):
            # the known y for every column
            yk = [self.interp_y[0][idx], self.interp_y[self.steps-1][idx]]

            #linear interpolation
            ip = np.interp(self.r_to_interpolate, self.known_t, yk)

            # sort the interpolated values into the array
            for r in range(0, len(self.r_to_interpolate)):
                self.interp_y[r][idx] = ip[r]

        # at second step, power vs. outside temp are interpolated using cubic splines
        # we want to have samples at every integer °C
        t = np.linspace(-30, 40, 71)
        # cubic spline interpolation of power curves
        for idx in range(0, len(self.r_to_interpolate)):
            #f = CubicSpline(known_x, interp_y[idx], bc_type='natural')
            f = Chebyshev.fit(self.known_x, self.interp_y[idx], deg = 8)
            self.max_power.append(f(t))

    def map(self,x,y):

        numrows = len(self.max_power)    # 3 rows in your example

        numcols = len(self.max_power[0]) # 2 columns in your example
        x=x-self.known_x[0]
        if x<0:
            x=0
        if x>70:
            x= 70
        y=y-self.known_t[0]
        if y<0:
            y=0
        if y> (self.steps-1):
            y=self.steps-1
        
        return self.max_power[int(y)][int(x)]


#map = PowerMap()

#plt.plot(t,np.transpose(map.max_power))
#plt.ylabel('Max Power')
#plt.xlabel('°C')
#plt.show()
