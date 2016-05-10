import csv
import matplotlib.pyplot as plt

states = ["california", "michigan", "new_york", 
					"ohio", "pennsylvania", "virginia", 
					"washington"]

states_upper = { "california": "CALIFORNIA", "michigan":"MICHIGAN", "new_york":"NEW YORK",
								"ohio":"OHIO", "pennsylvania":"PENNSYLVANIA", "virginia":"VIRGINIA",
								"washington":"WASHINGTON"} 

path = "data/"
# ignore year 2000
#d[state][year][period]=val
apples_info = {}
periods = {"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}

with open(path+"apple-2000-2010.csv") as f:
	reader = csv.DictReader(f)

	for row in reader:
		state = row['State'].lower().replace(" ", "_")
		if state not in apples_info:
			apples_info[state] = {}

		if row['Year'] not in apples_info[state]:
			apples_info[state][row['Year']] = [0.0] * 12

		if row['Value'] == ' (NA)':
			val = 0
		else:
			val = float(row['Value'])

		apples_info[state][row['Year']][periods[row['Period']]-1] = val

#print apples_data
# dict[state][year][month][mean]
state_temperatures = {}
for state in states:
	state_temperatures[state] = {}
	with open(path + "anual-" + state + "-2000-2010.csv") as f:
		reader = csv.DictReader(f)

		# date is formatted as YYYYmm. Ex: 200101
		# monthly mean temperature: MNTM
		for row in reader: 
			year = row["DATE"][:4]

			# ignore year 2000
			if year == '2000': continue

			if year not in state_temperatures[state]:
				state_temperatures[state][year] = [0.0] * 12 # each year contains a list of all temperatures for the given month	

			month = row["DATE"][4:]	
			m = int(month)

			# watch out for -9999
			mean = float(row["MNTM"])

			# -9999 means missing data. If data is missing, get the maximun mean otherwise minimum
			if mean < 0:
				mean = float(row["MMXT"])

			# if it still -9999 use the minimum
			if mean < 0:
				mean = float(row["MMNT"])

			state_temperatures[state][year][m-1] = mean

def print_state_temp_as_table(data):
	ms = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
	for s in data.keys():
		print "\t"*6,states_upper[s]
		print "*" * 100
		print "    \t", "\t".join(ms)
		print "_" * 100
		years = sorted(data[s].keys())
		for year in years:
			print year+"\t", "\t".join(map(str,data[s][year]))
		print "-" * 100	


print "^" * 43, "TEMPERATURES", "^" * 43
print_state_temp_as_table(state_temperatures)
print "#" * 43, "APPLE PRICES", "#" * 43
print_state_temp_as_table(apples_info)
