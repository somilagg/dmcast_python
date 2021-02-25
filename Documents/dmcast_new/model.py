import math
import csv

class daily_weather(object):

	'''
	starting from september 21st, get the average temp and rainfall each day
	
	matrix guide:
	#################

	self.main_matrix = hourly features from original dataset:
	 - 0:	month
	 - 1:	day
	 - 2:	hour
	 - 3:	airTempF
	 - 4:	precipInches
	 - 5:	leafWetness
	 - 6:	rhPercent
	 - 7:	windSpeed
	 - 8:	windDirDegrees
	 - 9:	solarRadLangleys
	 - 10:	soilTempF
	 - 11:	soilMoistM3M3
	 - 12:	dewpointF

	self.ret_matrix = daily features with tmp and prcp
	 - 0:	month
	 - 1:	day
	 - 2:	dlytemp
	 - 3:	dlyprcp
	 - 4:	els
	 - 5:	primary inf indicator
	 - 6:	incubation period indicaator
	 - 7:	incubation status (only happens if 6: exists)

	self.matrix_total = hourly features with tmp and prcp
	 - 0:	month
	 - 1:	day
	 - 2:	hour
	 - 3:	temp
	 - 4:	prcp

	 self.final_matrix = array with primary & secondary model features
	  - 0:	month
	  - 1:	day
	  - 2:	hour
	  - 3:	airTempF
	  - 4:	precipInches
	  - 5:	leafWetness
	  - 6:	rhPercent
	  - 7:	windSpeed
	  - 8:	windDirDegrees
	  - 9:	solarRadLangleys
	  - 10:	soilTempF
	  - 11:	soilMoistM3M3
	  - 12:	dewpointF
	  - 13: sp
	  - 14:	spmort
	  - 15: sv
	  - 16: infect
	  - 17: risk level 
	'''
	def __init__(self, end_m, end_d):

		# setting initial cultivars values to Concord
		self.A = 34.1
		self.B = 3.33
		self.k = 0.0041
		self.m = 2.075

		#array of number of days in month
		self.months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		#read in csv file to list
		with open('dmcast-sample-dataset-mccarthyFarm-20200701-20200931.csv', 'rt') as csv_file:
			reader = csv.reader(csv_file)
			inp = list(reader)
			inp.reverse()
		
		#initalizing variables
		curr_m = 7
		curr_d = 1
		index = 0
		self.ret_matrix = []
		self.ret_matrix_total = []
		self.main_matrix = []

		#goes until the end date is reached
		while end_m != curr_m or end_d != curr_d:

			#increase month if day limit is exceeded
			if curr_d > self.months[curr_m-1]:
				curr_m += 1
				curr_d = 1

			#starting information from csv file
			s = inp[index][0]
			curr_m = int(s[0:2])
			curr_d = int(s[3:5])

			#initializing variables
			total_temp = 0
			total_prcp = 0
			ret_arr = []
			orig_m = curr_m
			orig_d = curr_d

			#continue until next date is reached
			while orig_m == curr_m and orig_d == curr_d:
				ret_arr_total = []
				main_matrix_arr = []

				#add to total trackers
				total_temp += float(inp[index][1])
				total_prcp += float(inp[index][2])

				#to add to ret_matrix
				ret_arr_total.append(curr_m)
				ret_arr_total.append(curr_d)
				ret_arr_total.append(int(s[11:13]))
				temp_C = 5.0/9.0 * (float(inp[index][1]) - 32)
				ret_arr_total.append(round(temp_C,2))
				ret_arr_total.append(float(inp[index][2]))

				#to add to main_matrix
				main_matrix_arr.append(curr_m)
				main_matrix_arr.append(curr_d)
				main_matrix_arr.append(int(s[11:13]))
				main_matrix_arr.append(round(temp_C,2))

				try: main_matrix_arr.append(float(inp[index][2]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][3]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][4]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][5]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][6]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][7]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][8]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][9]))
				except: main_matrix_arr.append(0.0)
				try: main_matrix_arr.append(float(inp[index][10]))
				except: main_matrix_arr.append(0.0)

				#add to the matrices
				self.main_matrix.append(main_matrix_arr)
				self.ret_matrix_total.append(ret_arr_total)

				#iterate and get values of next row
				index += 1
				s = inp[index][0]
				curr_m = int(s[0:2])
				curr_d = int(s[3:5])

			#append month, day, total temperature, and total precipitation to array
			ret_arr.append(curr_m)
			ret_arr.append(curr_d)
			avgF = total_temp/24.0
			avgC = 5.0/9.0 * (avgF - 32)
			ret_arr.append(round(avgC,2))
			ret_arr.append(round(total_prcp,2))

			#append to 2d matrix of return values
			self.ret_matrix.append(ret_arr)
			index += 1

		self.primary_infection()
		self.incubation_period()
		self.cycle()

	def generate_els(self):

		for i in range(len(self.ret_matrix)):
			if self.ret_matrix[i][2] > 7:
				dday7 = 1
			else:
				dday7 = 0

			els = self.A * (1 + math.exp(self.B - self.k * dday7)) ** (1 / (1 - self.m))
			self.ret_matrix[i].append(round(els,2))

	def primary_infection(self):

		#generate els for day and add to matrix
		self.generate_els()

		#check for primary infection conditions
		for i in range(len(self.ret_matrix)):
			if self.ret_matrix[i][2] > 11.1 and self.ret_matrix[i][3] > 2.54 and self.ret_matrix[i][4] > 12:
				
				#add 1 to indicate primary model
				if len(self.ret_matrix[i]) == 6:
					self.ret_matrix[i][5] = 1
				else:
					self.ret_matrix[i].append(1)

				#add 1 to indicate seconday model 7 days from now
				if len(self.ret_matrix[i+7]) == 7:
					self.ret_matrix[i+7][6] = 1
				elif len(self.ret_matrix[i+7]) == 6:
					self.ret_matrix[i+7].append(1)
				else:
					self.ret_matrix[i+7].append(0)
					self.ret_matrix[i+7].append(1)

			else:
				self.ret_matrix[i].append(0)

	def incubation_period(self):

		for i in range(len(self.ret_matrix)):

			sincb = 0

			#its of length 7 if secondary infection was added
			if len(self.ret_matrix[i]) == 7:
				mo = self.ret_matrix[0]
				da = self.ret_matrix[1]

				total_pos = 23 * i
				
				hour_temp = self.ret_matrix_total[total_pos][3]
				if hour_temp > 8.0 and hour_temp < 35.0:
					y = 41.961 - 3.5794 * hour_temp + 0.09803 * hour_temp ** 2 - 0.0005341 * hour_temp ** 3

					if y > 0:
						rincb = (1.0/y)/24.0
					else:
						rincb = 0

					sincb += rincb

			#appends incubation status variable if threshold exceeded
			if sincb > 0.9999:
				self.ret_matrix[i].append(1)

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This subroutine estimates sporulation factor at each hour depending on  CC
	CC   temperature and relative humidity.                                      CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC  List of variables:                                                       CC
	CC   ISPRD = Hours of sporulation period: Sporulation starts when conditions CC
	CC          are favorable at least 4 hours (i.e., ISPD>=4) without any       CC
	CC          interuption                                                      CC
	CC   ISTMP = Average temperature during ISPRD                                CC
	CC   TMPSUM = Sum of hourly temperature during ISPRD                         CC
	CC   SP = Sporulation factor                                                 CC
	C*****************************************************************************C
	CCC==Sporulation occurs only during night (21:00-5:00) and relative humidity
	CCC==is greater than 90% 
	'''
	def sporulation(self, arr):
		
		sp = 0.0

		if (arr[2] > 21 or arr[2] <= 5) and (arr[6] >= 90):
			self.isprd += 1
			self.tmpsum += arr[3]
			self.istmp = self.tmpsum/self.isprd

			#determine sporulation factor
			if self.isprd >= 4:
				if self.istmp > 13.0 and self.istmp < 22.5:
					sp = max( (-642.0 + 53.7*self.istmp - 0.0356*self.istmp*self.istmp*self.istmp)/160.756 , 0.0 )
				elif self.istmp >= 22.5 and self.istmp <= 28.0:
					sp = 1.0
				elif self.istmp > 28.0 and self.istmp < 30.0:
					sp = 0.1
				else:
					sp = 0.0
			else:
				sp = 0.0
		else:
			sp = 0.0
			self.isprd = 0
			self.tmpsum = 0.0
			self.istmp = 0.0

		arr.append(sp)
		return arr

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This subroutine estimates mortality factor of spores and calculates     CC
	CC   survival factor at each hour depending on temperature and relative      CC
	CC   humidity.                                                               CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC   List of variables:                                                      CC
	CC    SP = Sporulation factor                                                CC
	CC    SV = Spore survival factor                                             CC
	CC    SPMORT = Spore mortality factor                                        CC
	C*****************************************************************************C
	'''
	def survival(self, arr):
		
		spmort = 0.0

		if self.sv < arr[11]:
			sv = arr[11]

		if arr[6] >= 90.0:
			if arr[3] <= 25.0:
				spmort = -0.00138 + 0.000496 * arr[3]
			else:
				spmort = -0.7711 + 0.03126 * arr[3]
		else:
			spmort = math.exp(-4.2057 - 0.2101 * arr[3] + 0.0095 * arr[3] * arr[3])

		spmort = max(spmort, 0.0)
		self.sv = self.sv - spmort
		self.sv = max(self.sv, 0.0)

		arr.append(spmort)
		arr.append(self.sv)
		return arr
	
	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This subroutine identifies favorable environmental conditions for       CC
	CC   infection process of the fungus.  Longer than 10 min of wetness period  CC
	CC   is necessary to make infection.                                         CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC   List of variables:                                                      CC
	CC    INFECT = Infection factor                                              CC
	CC    TSUMI = Sum of temperature during infection period                     CC
	CC    DF = Risk level of disease development                                 CC
	CC                                                                           CC
	CC    AVTMPI = Average temperature during the infection period               CC
	CC    WETPRD = Wetness period in minutes                                     CC
	CC    NI = Hours of a consecutive wetness period                             CC
	CC    IDSTRT = Starting date of wetness period                               CC
	CC    IHSTRT = Starting hour of wetness period                               CC
	CC    WETSUM = Sum of wetness period during infection period                 CC
	C*****************************************************************************C
	'''
	def infection(self, arr):
		
		tsumi = arr[10]
		infect = 0.0

		if tsumi < 45.0:
			infect = 0.0
		elif tsumi >= 45.0 and tsumi < 50.0:
			infect = 0.3/0.5 * (tsumi - 45.0) + 0.2
		elif tsumi >= 50.0 and tsumi < 71.0:
			infect = 0.5/21.0 * (tsumi - 50.0) + 0.5
		else:
			infect = 1.0

		arr.append(infect)
		arr.append(arr[len(arr)-2] * infect * 100)
		return arr

	def cycle(self):

		self.final_matrix = []

		self.isprd = 0
		self.tmpsum = 0.0
		self.istmp = 0.0

		self.sv = 0.0

		for i in range(len(self.main_matrix)):
			temp_arr = []
			temp_arr = self.sporulation(self.main_matrix[i])
			temp_arr = self.survival(temp_arr)
			temp_arr = self.infection(temp_arr)
			self.final_matrix.append(temp_arr)

if __name__ == '__main__':

	#return average temperature and precipitation from sep 1st to october 2nd
	daily_weather(8, 2)
	print("completed running model.py")