import csv

with open('dmcast-sample-dataset-mccarthyFarm-20200701-20200931.csv', 'rt') as csv_file:
	reader = csv.reader(csv_file)
	input_file = list(reader)

print(input_file[0])
print(input_file[1])
print(input_file[2])