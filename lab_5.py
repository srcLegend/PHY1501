import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def read_data(datafile: Path, zero_angle: float) -> tuple[np.ndarray, np.ndarray]:
	data: np.ndarray = np.genfromtxt(datafile, dtype = np.float64, delimiter = ',', skip_header = 1)

	currents: np.ndarray = data[:, 0]
	incident_angles: np.ndarray = data[:, 1] - zero_angle

	return currents, incident_angles

# Theta 2 in figure 5.2
def refraction_angle(n_1: float, n_2: float, incident_angle: float) -> float:
	return np.arcsin(n_1*np.sin(incident_angle)/n_2)

# Theta 3 in figure 5.2
def inner_incident_angle(refraction_angle: float):
	return np.pi/4 - refraction_angle

def parallel_reflectance(n_1: float, n_2: float, theta_1: float, theta_2: float) -> float:
	return ((n_2*np.cos(theta_1) - n_1*np.cos(theta_2))/(n_2*np.cos(theta_1) + n_1*np.cos(theta_2)))**2

def perpendicular_reflectance(n_1: float, n_2: float, theta_1: float, theta_2: float) -> float:
	return ((n_1*np.cos(theta_1) - n_2*np.cos(theta_2))/(n_1*np.cos(theta_1) + n_2*np.cos(theta_2)))**2

def refractive_index(theta_1c: float) -> float:
	return np.sqrt(2 + 2*np.sqrt(2)*np.sin(theta_1c) + 2*np.sin(theta_1c)**2)

def brewster_angle(n_1: float, n_2: float) -> float:
	return np.arctan(n_2/n_1)

if (__name__ == '__main__'):
	zero_angle = 268 + 2/3 + 10/60 # °
	theta_1c = 351 - zero_angle	   # °
	n_prisme = refractive_index(np.deg2rad(90 - theta_1c)) # 1.5151: https://refractiveindex.info/?shelf=glass&book=BK7&page=SCHOTT
	n_air = 1.00028759 # https://refractiveindex.info/?shelf=other&book=air&page=Borzsonyi

	laser_current = 1.01		# mA
	background_current = 0.0008 # mA


	uncertainties = {'laser_current':	   0.005,  # ± mA
					 'background_current': 0.0001, # ± mA
					 'critical_angle': 0.5/60, # ± °
					 'zero_angle':	   0.5/60} # ± °

	currents: dict[str, np.ndarray] = {}
	incident_angles: dict[str, np.ndarray] = {}

	datafiles = [f for f in Path('LAB5', 'data').iterdir() if (f.suffix == '.csv')]
	for datafile in datafiles:
		currents[datafile.stem], incident_angles[datafile.stem] = read_data(datafile, zero_angle)

	axes: list[list[plt.Axes]]
	figure, axes = plt.subplots(nrows = 1, ncols = 1, squeeze = False)
	axe = axes[0][0]

	axe.plot(incident_angles['parallel_reflection'])
	axe.set_xlim( 0, 40)
	axe.set_ylim(20, 90)

	axe.set(xlabel = 'Time (s)', ylabel = 'Voltage (mV)', title = 'About as simple as it gets, folks')
	axe.grid()

	figure.savefig(Path('LAB5', 'test.svg'))
