import math
import csv

class daily_weather(object):

	'''
	starting from september 21st, get the average temp and rainfall each day
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
				#add to total trackers
				total_temp += float(inp[index][1])
				total_prcp += float(inp[index][2])
				ret_arr_total.append(curr_m)
				ret_arr_total.append(curr_d)
				ret_arr_total.append(int(s[11:13]))
				temp_C = 5.0/9.0 * (float(inp[index][1]) - 32)
				ret_arr_total.append(round(temp_C,2))
				ret_arr_total.append(float(inp[index][2]))
				
				#iterate and get values of next row
				index += 1
				s = inp[index][0]
				curr_m = int(s[0:2])
				curr_d = int(s[3:5])
				self.ret_matrix_total.append(ret_arr_total)

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
			
	def generate_els(self):


		for i in range(len(self.ret_matrix)):
			if self.ret_matrix[i][2] > 7:
				dday7 = 1
			else:
				dday7 = 0

			els = self.A * (1 + math.exp(self.B - self.k * dday7)) ** (1 / (1 - self.m))
			self.ret_matrix[i].append(round(els,2))

	# def calculate_second_infection(self, mon, day):
		
	# 	max_days = self.months[mon]
	# 	sec_inf_day = day + 7

	# 	if sec_inf_day > max_days:
	# 		sec_inf_day -= max_days

	# 		if mon == 12:
	# 			mon = 1
	# 		else:
	# 			mon += 1

	# 	return (mon, sec_inf_day)

	def primary_infection(self):

		self.generate_els()

		for i in range(len(self.ret_matrix)):
			if self.ret_matrix[i][2] > 11.1 and self.ret_matrix[i][3] > 2.54 and self.ret_matrix[i][4] > 12:
				self.ret_matrix[i].append(1)

				#(m, d) = self.calculate_second_infection(self.ret_matrix[i][0], self.ret_matrix[i][1])
				self.ret_matrix[i+7].append(1)
			else:
				self.ret_matrix[i].append(0)

	def secondary_infection(self):
		
		for i in range(len(self.ret_matrix)):
			if len(self.ret_matrix[i]) == 6:
				mo = self.ret_matrix[0]
				da = self.ret_matrix[1]

				total_pos = 23 * i
				sincb = 0

				hour_temp = self.ret_matrix_total[total_pos][3]
				if hour_temp > 8.0 and hour_temp < 35.0:
					y = 41.961 - 3.5794 * temp + 0.09803 * temp ** 2 - 0.0005341 * temp ** 3

					if y > 0:
						rincb = (1.0/y)/24.0
					else:
						rincb = 0

					sincb += rincb

			if sincb > 0.9999:
				self.ret_matrix[i].append(1)


class phenology_model(object):

	def __init__(self):
		pass

class hourly_weather(object):

	def __init__(self):
		pass

class dmcast(object):

	def __init__(self):
		pass

	def initialization(self):
		pass

	def oospoure_maturation_model(self):
		pass

	def primary_infection_model(self):
		pass

	def primary_infection_date(self):
		pass

	def secondary_infection_models(self):
		pass

	def output(self):
		pass
	'''
	ra = cumulative value of rain effect
	'''
	def days_osp_from_ra(self, ra):
		d = 118 - 0.3 * ra
		v = 13.5 + 0.02 * ra
		return d, v

	'''
	D = mean days from Jan 1st required for ospore maturation
	v = std dev days from Jan 1st required for ospore maturation
	'''
	def prob_osp(self, D, v, k):
		ans = 1 / ( v * math.sqrt( 2 * math.pi ) )
		exp = -0.5 * ( k * D / v ) ** 2
		ans *= math.exp(exp)
		return ans


if __name__ == '__main__':

	#return average temperature and precipitation from sep 1st to october 2nd
	daily_weather(8, 2)