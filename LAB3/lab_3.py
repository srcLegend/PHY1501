import numpy as np
from pathlib import Path

# All uncertainty formulas taken from "https://chem.libretexts.org/Bookshelves/Analytical_Chemistry/Supplemental_Modules_(Analytical_Chemistry)/Quantifying_Nature/Significant_Digits/Propagation_of_Error"
def propagated_uncertainty(propagation_type: str, **kwargs) -> float:
	"""	Returns confidence interval based on formula type\n
		Multiply by absolute final value if multiplicative or exponential"""

	if (propagation_type == 'additive'):
		uncertainties: list[float] = kwargs['uncertainties']
		return np.sqrt(np.sum([u**2 for u in uncertainties]))

	elif (propagation_type == 'multiplicative'):
		uncertainties: list[float] = kwargs['uncertainties']
		values: list[float] = kwargs['values']
		return np.sqrt(np.sum([(u/v)**2 for u, v in zip(uncertainties, values)]))

	elif (propagation_type == 'exponential'):
		exponent: float = kwargs['exponent']
		uncertainty: float = kwargs['uncertainty']
		value: float = kwargs['value']
		return exponent*uncertainty/value

def sound_velocity(frequencies: np.ndarray, tube_length: float) -> np.ndarray:
	"""Returns `c` values of equation (3.9) for each frequency `v`"""
	return np.asarray([2*frequency*tube_length/(n + 1) for n, frequency in enumerate(frequencies) if (frequency > 0)], dtype = np.float64)

def gamma(sound_velocity: float, molar_mass: float) -> float:
	"""Returns `γ` values of equation (3.6)"""
	return molar_mass*(sound_velocity**2)/(R_CONSTANT*TEMPERATURE)

if (__name__ == '__main__'):
	TEMPERATURE = 22 + 273.15	   # Kelvin
	R_CONSTANT = 8.31446261815324  # J/(mol*K)
	MOLAR_MASS = {'air':  28.97,   # g/mol: https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
				  'Ar':   39.948,  # https://webbook.nist.gov/cgi/cbook.cgi?ID=7440-37-1
				  'CO2':  44.0095, # https://webbook.nist.gov/cgi/cbook.cgi?ID=124-38-9
				  'SF6': 146.055}  # https://webbook.nist.gov/cgi/cbook.cgi?ID=2551-62-4

	tube_length: dict = {'long': 0.491, 'short': 0.291} # m
	expirement_uncertainties: dict = {'frequency': 4, # ± Hz
									  'temperature': 1, # ± K
									  'tube_length': 0.001} # ± m

	frequencies: dict[str, np.ndarray] = {}
	gamma_values: dict[str, float] = {}
	sound_velocities: dict[str, float] = {}
	derived_uncertainties: dict[str, dict[str, float]] = {'gamma_values': {}, 'sound_velocities': {}}

	datafiles = [f for f in Path('LAB3', 'data').iterdir() if (f.suffix == '.csv')]
	for datafile in datafiles:
		frequencies[datafile.stem] = np.genfromtxt(datafile, dtype = np.uint32, delimiter = ',', skip_header = 1)
		gas = datafile.stem.rsplit('_', 1)[1]
		length = datafile.stem.split('_', 1)[0]

		# Temporary, sound velocities for each frequency
		temp_c = sound_velocity(frequencies[datafile.stem], tube_length[length])

		sound_velocities[datafile.stem] = temp_c.mean()
		gamma_values[datafile.stem] = gamma(sound_velocities[datafile.stem], MOLAR_MASS[gas]/1000)


		# Temporary, calculated sound velocity uncertainties for each frequency
		sv_uncertainties: list[float] = []
		for f, c in zip(np.trim_zeros(frequencies[datafile.stem]), temp_c):
			sv_uncertainties.append(c*propagated_uncertainty('multiplicative',
															 uncertainties = [expirement_uncertainties['frequency'], expirement_uncertainties['tube_length']],
															 values = [f, tube_length[length]]))

		# Temporary, nominator uncertainty of mean sound velocity
		temp_s = propagated_uncertainty('additive', uncertainties = sv_uncertainties)
		derived_uncertainties['sound_velocities'][datafile.stem] = sound_velocities[datafile.stem]*propagated_uncertainty('multiplicative',
																														  uncertainties = [temp_s, 0],
																														  values = [np.sum(temp_c), len(temp_c)])

		# Temporary, uncertainty of the power component
		temp_p = sound_velocities[datafile.stem]*propagated_uncertainty('exponential',
																		exponent = 2,
																		uncertainty = derived_uncertainties['sound_velocities'][datafile.stem],
																		value = sound_velocities[datafile.stem])

		derived_uncertainties['gamma_values'][datafile.stem] = gamma_values[datafile.stem]*propagated_uncertainty('multiplicative',
																												  uncertainties = [temp_p, expirement_uncertainties['temperature']],
																												  values = [sound_velocities[datafile.stem], TEMPERATURE])

	# Memory cleanup
	del c, f, datafile, datafiles, gas, length, sv_uncertainties, temp_c, temp_p, temp_s

	for k, sv, gv in zip(frequencies.keys(), sound_velocities.values(), gamma_values.values()):
		gas = k.rsplit('_', 1)[1]
		length = k.split('_', 1)[0]

		print(f"{length.capitalize()} tube, filled with {gas}")
		print(f"	Mean sound velocity within: {sv:0.0f} ± {derived_uncertainties['sound_velocities'][k]:0.1f} m/s")
		print(f"	γ (Cp/Cv) value within: {gv:0.3f} ± {derived_uncertainties['gamma_values'][k]:0.3f}")
