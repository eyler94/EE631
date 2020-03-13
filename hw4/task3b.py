#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
# from numpy.polynomial import polynomial as polyfit

points_3d = np.load('points_3d.npy')

points_catcher = points_3d-np.array([11.5, 29.5, 21.5])

fig1 = plt.figure(1)
x_points = points_catcher.T[0][0]
z_points = points_catcher.T[2][0]
legend_str = []
time = 0

coef = np.polyfit(z_points, x_points, 2)
x_func = np.poly1d(coef)
t = np.linspace(z_points[0],0,100)
x = x_func(t)

for point_z, point_x in zip(z_points,x_points):
    plt.plot(point_z,point_x,'o')
    legend_str.append(f"time: {time}")
    time +=1
plt.plot(t,x)
plt.legend(legend_str)
plt.ylabel("x")
plt.xlabel("z")
plt.title("z vs. x")

fig2 = plt.figure(2)
y_points = points_catcher.T[1][0]
legend_str = []
time = 0

coef = np.polyfit(z_points, y_points, 2)
y_func = np.poly1d(coef)
t = np.linspace(z_points[0],0,100)
y = y_func(t)

for point_z, point_y in zip(z_points,y_points):
    plt.plot(point_z,point_y,'o')
    legend_str.append(f"time: {time}")
    time +=1
plt.plot(t,y)
plt.legend(legend_str)
plt.ylabel("y")
plt.xlabel("z")
plt.title("z vs. y")
plt.show()
