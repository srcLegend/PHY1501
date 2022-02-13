from mpmath import mp, mpf

mp.dps = 100 # Decimal places to use in calculations

class Measurement:
	value: mpf
	uncertainty: mpf

	v_decimals: int = None
	v_significant_digits: int = None
	u_significant_digits: int = 1

	def __init__(self, value: str, uncertainty: str, v_decimals: int = None, v_significant_digits: int = None, u_significant_digits: int = None) -> None:
		if (v_decimals is None) and (v_significant_digits is None):
			raise Exception('Neither of the decimal precision nor the amount of significant digits have been set')

		self.value = mpf(value)
		self.uncertainty = mpf(uncertainty)

		if v_decimals is not None:
			self.v_decimals = v_decimals

			if self.v_decimals == 0:
				v_string = str(int(mp.floor(self.value)))
				self.v_significant_digits = len(v_string)
			else:
				v_string = str(self.value).split('.')
				self.v_significant_digits = len(v_string[0]) + self.v_decimals

		if v_significant_digits is not None:
			self.v_significant_digits = v_significant_digits

			if '.' in str(self.value):
				v_string = str(self.value).split('.')
				self.v_decimals = (self.v_significant_digits - len(v_string[0])) if (self.v_significant_digits > len(v_string[0])) else 0
			else:
				self.v_decimals = 0

		if u_significant_digits is not None:
			self.u_significant_digits = u_significant_digits

	def __str__(self) -> str:
		value = mp.nstr(self.value, n = self.v_significant_digits, min_fixed = -mp.inf, max_fixed = mp.inf, strip_zeros = False)
		uncertainty = mp.nstr(self.uncertainty, n = self.u_significant_digits, min_fixed = -mp.inf, max_fixed = mp.inf, strip_zeros = True)

		u1, u2 = [int(u) for u in uncertainty.split('.')]
		if ((u1 == 1) and (u2 == 0)) or ((u1 == 0) and (u2 == 1)):
			uncertainty = mp.nstr(self.uncertainty, n = self.u_significant_digits + 1, min_fixed = -mp.inf, max_fixed = mp.inf, strip_zeros = False)
		elif int(mpf(uncertainty)) == mpf(uncertainty):
				value = int(mp.nint(value))
				uncertainty = int(mpf(uncertainty))

		return f'{value} ± {uncertainty}'

	def __add__(self, other):
		if isinstance(other, Measurement):
			value = self.value + other.value
			uncertainty = mp.sqrt(self.uncertainty**2 + other.uncertainty**2)
			return Measurement(value, uncertainty, v_decimals = min(self.v_decimals, other.v_decimals))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value + other
			return Measurement(value, self.uncertainty, v_decimals = self.v_decimals)

	def __radd__(self, other):
		if isinstance(other, Measurement):
			value = self.value + other.value
			uncertainty = mp.sqrt(self.uncertainty**2 + other.uncertainty**2)
			return Measurement(value, uncertainty, v_decimals = min(self.v_decimals, other.v_decimals))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value + other
			return Measurement(value, self.uncertainty, v_decimals = self.v_decimals)

	def __sub__(self, other):
		if isinstance(other, Measurement):
			value = self.value - other.value
			uncertainty = mp.sqrt(self.uncertainty**2 + other.uncertainty**2)
			return Measurement(value, uncertainty, v_decimals = min(self.v_decimals, other.v_decimals))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value - other
			return Measurement(value, self.uncertainty, v_decimals = self.v_decimals)

	def __rsub__(self, other):
		if isinstance(other, Measurement):
			value = self.value - other.value
			uncertainty = mp.sqrt(self.uncertainty**2 + other.uncertainty**2)
			return Measurement(value, uncertainty, v_decimals = min(self.v_decimals, other.v_decimals))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value - other
			return Measurement(value, self.uncertainty, v_decimals = self.v_decimals)

	def __mul__(self, other):
		if isinstance(other, Measurement):
			value = self.value*other.value
			uncertainty = abs(value)*mp.sqrt((self.uncertainty/self.value)**2 + (other.uncertainty/other.value)**2)
			return Measurement(value, uncertainty, v_significant_digits = min(self.v_significant_digits, other.v_significant_digits))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value*other
			uncertainty = abs(other)*self.uncertainty
			return Measurement(value, uncertainty, v_significant_digits = self.v_significant_digits)

	def __rmul__(self, other):
		if isinstance(other, Measurement):
			value = self.value*other.value
			uncertainty = abs(value)*mp.sqrt((self.uncertainty/self.value)**2 + (other.uncertainty/other.value)**2)
			return Measurement(value, uncertainty, v_significant_digits = min(self.v_significant_digits, other.v_significant_digits))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value*other
			uncertainty = abs(other)*self.uncertainty
			return Measurement(value, uncertainty, v_significant_digits = self.v_significant_digits)

	def __truediv__(self, other):
		if isinstance(other, Measurement):
			value = self.value/other.value
			uncertainty = abs(value)*mp.sqrt((self.uncertainty/self.value)**2 + (other.uncertainty/other.value)**2)
			return Measurement(value, uncertainty, v_significant_digits = min(self.v_significant_digits, other.v_significant_digits))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value/other
			uncertainty = self.uncertainty/abs(other)
			return Measurement(value, uncertainty, v_significant_digits = self.v_significant_digits)

	def __rtruediv__(self, other):
		if isinstance(other, Measurement):
			value = self.value/other.value
			uncertainty = abs(value)*mp.sqrt((self.uncertainty/self.value)**2 + (other.uncertainty/other.value)**2)
			return Measurement(value, uncertainty, v_significant_digits = min(self.v_significant_digits, other.v_significant_digits))

		elif isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value/other
			uncertainty = self.uncertainty/abs(other)
			return Measurement(value, uncertainty, v_significant_digits = self.v_significant_digits)

	def __pow__(self, other):
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			value = self.value**other
			uncertainty = abs(other*self.value**(other - 1))*self.uncertainty
			return Measurement(value, uncertainty, v_significant_digits = self.v_significant_digits)

	def __lt__(self, other) -> bool:
		if isinstance(other, Measurement):
			return self.value < other.value
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			return self.value < other

	def __le__(self, other) -> bool:
		if isinstance(other, Measurement):
			return self.value <= other.value
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			return self.value <= other

	def __eq__(self, other) -> bool:
		if isinstance(other, Measurement):
			return self.value == other.value
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			return self.value == other

	def __ne__(self, other) -> bool:
		if isinstance(other, Measurement):
			return self.value != other.value
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			return self.value != other

	def __gt__(self, other) -> bool:
		if isinstance(other, Measurement):
			return self.value > other.value
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			return self.value > other

	def __ge__(self, other) -> bool:
		if isinstance(other, Measurement):
			return self.value >= other.value
		if isinstance(other, int) or isinstance(other, float) or isinstance(other, mpf):
			return self.value >= other
