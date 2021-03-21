import math
import csv

class daily_weather(object):

	'''	
	system design (basic guide):
	##################################

	1. 	create matrix with daily temp, prcp
	2. 	create matrix with hourly temp, prcp
	3. 	call primary infection
	4. 	generate els variable
	5. 	include primary infection variable
	6. 	include secondary infection variable (if applicable)
	7. 	call incubation period
	8. 	sets incubation status if secondary infection variable is 1
	9. 	calls cycle
	10. inside cycle, calls sporulation and adds sporulation factor
	11. inside cycle, calls survival and adds spore survival factor and spore mortality factor
	12. inside cycle, calls infection and adds infection factor and risk level of disease development
	13. fin!

	matrix guide:
	##################################

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

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method initializes the model and reads in data from the NEWA 		 CC
	CC   dataset.                                      							 CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC  List of variables:                                                       CC
	CC   END_M = ending month of data traversal									 CC
	CC   END_D = ending day of data traversal                             		 CC 
	CC   TEST = boolean indicating test mode -> False by default				 CC
	CC   TEST_METHOD_NUM = if TEST is True, indicates which test case to run 	 CC                                                
	C*****************************************************************************C
	'''
	def __init__(self, end_m, end_d, test=False, test_method_num=0, els=13):

		self.print_introduction(test)

		self.els = els

		# setting initial cultivars values to Chardonnay
		self.A = 35.2
		self.B = 1.44
		self.k = 0.0029
		self.m = 1.438

		#array of number of days in month
		self.months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		if test_method_num ==  0:
			file_name = 'dmcast-sample-dataset-mccarthyFarm-20200701-20200931.csv'
		else:
			file_name = self.run_test(test_method_num)

		#read in csv file to list
		with open(file_name, 'rt') as csv_file:
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
		while (end_m != curr_m or end_d != curr_d) and index < len(inp):

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
			while orig_m == curr_m and orig_d == curr_d and index < len(inp):
				ret_arr_total = []
				main_matrix_arr = []

				#add to total trackers
				total_temp += float(inp[index][1])
				total_prcp += float(inp[index][2]) * 25.4

				#to add to ret_matrix
				ret_arr_total.append(curr_m)
				ret_arr_total.append(curr_d)
				ret_arr_total.append(int(s[11:13]))
				temp_C = 5.0/9.0 * (float(inp[index][1]) - 32)
				ret_arr_total.append(round(temp_C,2))
				ret_arr_total.append(float(inp[index][2]) * 25.4)

				#to add to main_matrix
				main_matrix_arr.append(curr_m)
				main_matrix_arr.append(curr_d)
				main_matrix_arr.append(int(s[11:13]))
				main_matrix_arr.append(round(temp_C,2))

				try: main_matrix_arr.append(float(inp[index][2]) * 25.4)
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
				if(index < len(inp)):
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

		print("#	-------------------------------------------------	#")
		print("#	Successfully calculated primary infection model.")
		print("#	-------------------------------------------------	#")
		print ""

		self.incubation_period()

		print("#	-------------------------------------------------	#")
		print("#	Successfully calculated incubation period.")
		print("#	-------------------------------------------------	#")
		print ""

		self.cycle()

		print("#	-------------------------------------------------	#")
		print("#	Successfully calculated CYCLE.")
		print("#	-------------------------------------------------	#")
		print ""

		print('Primary infection conditions satisfied on:')
		if len(self.primary_list) == 0:
			print("NONE")
		else:
			print(self.primary_list)

		print ""
		print('Secondary infection conditions satisfied on:')
		if len(self.secondary_list) == 0:
			print("NONE")
		else:
			print(self.secondary_list)

	def return_lists(self):
		return self.primary_list, self.secondary_list

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method prints out the introduction for the user.					 CC                                      							 CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC  List of variables:                                                       CC
	CC   TEST = boolean indicating test run or not                               CC                                                 CC
	C*****************************************************************************C
	'''
	def print_introduction(self, test):
		
		print ""
		print("#	-------------------------------------------------	#")
		print("#	Welcome to the updated version of DMCast!")
		print("#	Made by Somil Aggarwal & Katie Gold")

		if test == True:
			print("#	Running version: TEST")
		else:
			print("#	Running version: NORMAL")

		print("#	-------------------------------------------------	#")
		print ""

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method generates the ELS stages of each day in the dataset based	 CC
	CC   on information from the cultivars of the plant.                         CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	'''
	def generate_els(self):

		#CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
		# POTENTIAL FOR CV INTEGRATION OF CANOPY OBSERVATION FROM PROXIMAL DATASTREAM
		
		for i in range(len(self.ret_matrix)):
			if self.ret_matrix[i][2] > 7:
				dday7 = 1
			else:
				dday7 = 0

			#dday7 = 5
			'''
			A= 35
			B= 1.5
			k= 0.003
			m=1.5
			'''
			# expo = self.B - self.k * dday7
			# pwr = 1 / (1 - self.m)
			# els = self.A * (1 + math.exp(expo)) ** pwr
			# #		35    * 0.03)
			# els = 13
			self.ret_matrix[i].append(round(self.els,2))

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method detects dates for primary infection based on sufficient	 CC
	CC   temperature, precipitation, and ELS thresholds.                         CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	'''
	def primary_infection(self):

		#generate els for day and add to matrix
		self.generate_els()

		#check for primary infection conditions
		self.primary_list = []
		self.secondary_list = []
		for i in range(len(self.ret_matrix)):
			if self.ret_matrix[i][2] > 11.1 and self.ret_matrix[i][3] > 2.54 and self.ret_matrix[i][4] > 12:
				
				#add 1 to indicate primary model
				self.primary_list.append((self.ret_matrix[i][0], self.ret_matrix[i][1]))
				if len(self.ret_matrix[i]) == 6:
					self.ret_matrix[i][5] = 1
				else:
					self.ret_matrix[i].append(1)

				#!--- look into modifying this factor since this is a proxy for growers - not actual indicator ---!
				#!--- move to spore mortality (?) ---!
				#add 1 to indicate seconday model 7 days from now
				if i+7 < len(self.ret_matrix):
					if len(self.ret_matrix[i+7]) == 7:
						self.ret_matrix[i+7][6] = 1
					elif len(self.ret_matrix[i+7]) == 6:
						self.ret_matrix[i+7].append(1)
					else:
						self.ret_matrix[i+7].append(0)
						self.ret_matrix[i+7].append(1)
						self.secondary_list.append((self.ret_matrix[i+7][0], self.ret_matrix[i+7][1]))

			else:
				self.ret_matrix[i].append(0)

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method detects dates for primary infection based on hourly		 CC 
	CC   information of the temperature and a regression model.                  CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	'''
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
				self.secondary_list.append((ret_matrix[0], ret_matrix[1]))

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method estimates sporulation factor at each hour depending on      CC
	CC   temperature and relative humidity.                                      CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC  List of variables:                                                       CC
	CC   ARR = input information from NEWA dataset                               CC
	C*****************************************************************************C
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

		arr.append(round(sp,2))
		return arr

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method estimates mortality factor of spores and calculates         CC
	CC   survival factor at each hour depending on temperature and relative      CC
	CC   humidity.                                                               CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC   List of variables:                                                      CC
	CC    ARR = input information from NEWA dataset                              CC
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

		arr.append(round(spmort,2))
		arr.append(round(self.sv,2))
		return arr
	
	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method identifies favorable environmental conditions for the       CC
	CC   infection process of the fungus.  Longer than 10 min of wetness period  CC
	CC   is necessary to make infection.                                         CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC   List of variables:                                                      CC
	CC    ARR = input information from NEWA dataset                              CC
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

		arr.append(round(infect,2))
		arr.append(round(arr[len(arr)-2] * infect * 100,2))
		if (arr[len(arr)-1] > 0):
			print("greater than 0")
		return arr

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method calls the sub methods of CYCLE: sporulation, survival, 	 CC
	CC	 and infection.                                         				 CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	'''
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

	'''
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	CC   This method runs the tests for the model.                               CC
	CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
	C*****************************************************************************C
	CC   List of variables:                                                      CC
	CC    TEST_NUM = test number to run on 				                         CC
	C*****************************************************************************C
	'''

	def generate_test_dataset(self, test_num, input_arr):

		file_name = 'test_input_' + str(test_num) + '.csv'
		with open(file_name, mode='w') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

			for d in range(0, 31):
				d_str = ('0' + str(d)) if (d < 10) else str(d)
				for h in range(1, 24):
					h_str = ('0' + str(h)) if (h < 10) else str(h)
					t = '07/' + str(d_str) + '/2020 ' + str(h_str) + ':00 EDT'

					input_arr[0] = t
					csv_writer.writerow(input_arr)

			csv_file.close()

		return file_name

	def run_test(self, test_num):

		if test_num == 2:

			#sufficient temperature for primary - nothing else
			temp_arr = ['', '100', '0', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, temp_arr)

		elif test_num == 3:

			#sufficient precipitation for primary - nothing else
			prcp_arr = ['', '0', '3', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, prcp_arr)

		elif test_num == 4:

			#sufficient els for primary - nothing else
			els_arr = ['', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, els_arr)
			
		elif test_num == 5:

			#sufficient temperature and precipitation for primary - nothing else
			temp_and_prcp_arr = ['', '100', '3', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, temp_and_prcp_arr)

		elif test_num == 6:

			#sufficient temperature and els for primary - nothing else
			temp_and_els_arr = ['', '100', '0', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, temp_and_els_arr)

		elif test_num == 7:

			#sufficient precipitation and els for primary - nothing else
			prcp_and_els_arr = ['', '0', '3', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, prcp_and_els_arr)

		elif test_num == 8:

			#all sufficient primary conditions
			all_sufficient_arr = ['', '100', '3', '0', '0', '0', '0', '0', '0', '0', '0']
			return self.generate_test_dataset(test_num, all_sufficient_arr)

if __name__ == '__main__':

	#return average temperature and precipitation from sep 1st to october 2nd
	daily_weather(0, 0, True, 2)
	#daily_weather(8, 2)
	print ""
	print("#	-------------------------------------------------	#")
	print("#	Successfully completed running model.py")
	print("#	-------------------------------------------------	#")
