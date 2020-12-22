import os

class targets:
	def __init__(self):
		pass

	def default(self,row):
		return int(row._c4)

	def AMDCI(self,row):
		if (int(row._c4) == 1) and (int(row._c3) > 26):
			return 1
		else:
			return 0

	def preClinical(self,row):
		if int(row._c4) == 1 and int(row._c1) < 60:
			return 1
		else:
			return 0

	def MMSE(self,row):
		mmse = int(row._c3)
		if mmse > 24:
			return 0
		if mmse > 20 and mmse <= 24:
			return 1
		if mmse > 13 and mmse <= 20:
			return 2
		if mmse <= 13:
			return 3