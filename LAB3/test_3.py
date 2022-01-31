import numpy as np

def sound_velocity(frequency: float, tube_length: float) -> float:
	"""Returns `c` value of equation (3.9), assuming `n = 1`"""
	return 2*frequency*tube_length

def multiplicative_ci(values: list[float], uncertainties: list[float]) -> float:
	"""Multiplicative confidence interval. Multiply by the absolute final value"""
	return np.sqrt(np.sum([(sigma_v/v)**2 for v, sigma_v in zip(values, uncertainties)]) + 2*(np.prod(uncertainties)**2)/np.prod(values))

fundamental_frequency = 500 # Hz
tube_length = 0.300 # m

uncertainties = {'fundamental_frequency': 2.5, # ± Hz
				 'tube_length': 0.003} # ± m

c_gas = sound_velocity(fundamental_frequency, tube_length)
uncertainties['c_gas'] = c_gas*multiplicative_ci([fundamental_frequency, tube_length], [*uncertainties.values()])

print(f"c = {c_gas:0.0f} ± {uncertainties['c_gas']:0.0f} m/s")
