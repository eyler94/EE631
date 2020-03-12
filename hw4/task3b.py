#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

points_3d = np.load('points_3d.npy')

points_catcher = points_3d-np.array([11.5, 29.5, 21.5])

fig1 = plt.figure(1)
x_points = points_catcher.T[0][0]
z_points = points_catcher.T[2][0]
legend_str = []
time = 0
for point_z, point_x in zip(z_points,x_points):
    plt.plot(point_z,point_x,'o')
    legend_str.append(f"time: {time}")
    time +=1
plt.legend(legend_str)
plt.title("z vs. x")

fig2 = plt.figure(2)
y_points = points_catcher.T[1][0]
legend_str = []
time = 0
for point_z, point_y in zip(z_points,y_points):
    plt.plot(point_z,point_y,'o')
    legend_str.append(f"time: {time}")
    time +=1
plt.legend(legend_str)
plt.title("z vs. y")
plt.show()
