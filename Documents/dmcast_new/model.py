import math
import csv

class daily_weather(object):

	'''
	date = [#,#]
	starting from september 21st, get the average temp and rainfall each day
	'''
	def __init__(self, date):

		#array of number of days in month
		months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

		#read in csv file to list
		with open('dmcast-sample-dataset-mccarthyFarm-20200701-20200931.csv', 'rt') as csv_file:
			reader = csv.reader(csv_file)
			inp = list(reader)
			inp.reverse()

		#target end date
		end_m = 8
		end_d = 2
		
		#initalizing variables
		curr_m = 7
		curr_d = 1
		index = 0
		ret_matrix = []

		#goes until the end date is reached
		while end_m != curr_m or end_d != curr_d:

			#increase month if day limit is exceeded
			if curr_d > months[curr_m-1]:
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

				#add to total trackers
				total_temp += float(inp[index][1])
				total_prcp += float(inp[index][2])
				
				#iterate and get values of next row
				index += 1
				s = inp[index][0]
				curr_m = int(s[0:2])
				curr_d = int(s[3:5])

			#append month, day, total temperature, and total precipitation to array
			ret_arr.append(curr_m)
			ret_arr.append(curr_d)
			ret_arr.append(total_temp)
			ret_arr.append(total_prcp)

			#append to 2d matrix of return values
			ret_matrix.append(ret_arr)
			index += 1

		print(ret_matrix)
			

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
	daily_weather(3)