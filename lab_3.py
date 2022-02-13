import csv
from classes import Measurement
from mpmath import mp, mpf
from pathlib import Path

mp.dps = 100 # Decimal places to use in calculations

def sound_velocity(frequencies: list[Measurement], tube_length: Measurement) -> Measurement:
	"""Returns the average of the `c` values of equation (3.9) for each frequency `v`"""
	velocities = [2*f*tube_length/(n + 1) for n, f in enumerate(frequencies) if (f.value > 0)]
	return sum(velocities)/len(velocities)

def gamma(sound_velocity: Measurement, molar_mass: mpf) -> Measurement:
	"""Returns `γ` values of equation (3.6)"""
	return molar_mass*(sound_velocity**2)/(R_CONSTANT*TEMPERATURE)

if (__name__ == '__main__'):
	TEMPERATURE = Measurement(22 + mpf('273.15'), 1, v_decimals = 0) # Kelvin
	R_CONSTANT = mpf('8.31446261815324') # J/(mol*K)
	MOLAR_MASS = {'air': mpf('28.97'),	 # g/mol: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
				  'Ar':	 mpf('39.948'),	 # https://webbook.nist.gov/cgi/cbook.cgi?ID=7440-37-1
				  'CO2': mpf('44.0095'), # https://webbook.nist.gov/cgi/cbook.cgi?ID=124-38-9
				  'SF6': mpf('146.055')} # https://webbook.nist.gov/cgi/cbook.cgi?ID=2551-62-4

	tube_length: dict = {'long':  Measurement(mpf('0.514'), mpf('0.005'), v_significant_digits = 3) - Measurement(mpf('0.023'), mpf('0.005'), v_significant_digits = 3), # m
						 'short': Measurement(mpf('0.574'), mpf('0.005'), v_significant_digits = 3) - Measurement(mpf('0.283'), mpf('0.005'), v_significant_digits = 3)} # m

	frequencies: dict[str, list[Measurement]] = {}
	gamma_values: dict[str, Measurement] = {}
	sound_velocities: dict[str, Measurement] = {}

	datafiles = [f for f in Path('LAB3\\data').iterdir() if (f.suffix == '.csv')]
	for datafile in datafiles:
		with open(datafile, 'r') as csvfile:
			rows = csv.reader(csvfile)
			next(rows) # Skips header

			frequencies[datafile.stem] = []
			[frequencies[datafile.stem].append(Measurement(int(row[0]), 4, v_decimals = 0)) for row in rows]

		gas = datafile.stem.rsplit('_', 1)[1]
		length = datafile.stem.split('_', 1)[0]

		if gas not in sound_velocities:
			sound_velocities[gas] = sound_velocity(frequencies[datafile.stem], tube_length[length])
		else:
			v1 = sound_velocities[gas]
			v2 = sound_velocity(frequencies[datafile.stem], tube_length[length])
			sound_velocities[gas] = (v1 + v2)/2

	gamma_values = {gas: gamma(sv, MOLAR_MASS[gas]/1000) for gas, sv in sound_velocities.items()}

	del datafile, datafiles, gas, length, v1, v2 # Memory cleanup

	for sv, gv in zip(sound_velocities.items(), gamma_values.items()):
		print(f"Mean sound velocity within {sv[0]}: {sv[1]} m/s")
		print(f"γ (Cp/Cv) value within {gv[0]}: {gv[1]}")
