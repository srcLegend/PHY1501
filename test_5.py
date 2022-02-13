import matplotlib.pyplot as plt
import numpy as np

# Theta 1
incident_angles = np.arange(20, 81, 1, dtype = np.float64)*np.pi/180

# Theta 2
def refraction_angle(n1: float, n2: float, incident_angle: float) -> float:
	return np.arcsin(n1*np.sin(incident_angle)/n2)

def perpendicular_reflectance(n1, n2, theta1, theta2):
	return ((n1*np.cos(theta1) - n2*np.cos(theta2))/(n1*np.cos(theta1) + n2*np.cos(theta2)))**2

def parallel_reflectance(n1, n2, theta1, theta2):
	return ((n2*np.cos(theta1) - n1*np.cos(theta2))/(n2*np.cos(theta1) + n1*np.cos(theta2)))**2

theta3 = lambda theta2: np.pi/4 - theta2








# Data for plotting
s = 1 + np.sin(2*np.pi*incident_angles)

axe: plt.Axes
figure, axe = plt.subplots(nrows = 1, ncols = 1, figsize = (16, 12))
axe.plot(incident_angles, s)

axe.set(xlabel = 'Time (s)', ylabel = 'Voltage (mV)', title = 'About as simple as it gets, folks')
axe.grid()

plt.show()
