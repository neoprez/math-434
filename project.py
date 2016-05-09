import csv
from collections import defaultdict

states = ["california", "michigan", "new_york", 
					"ohio", "pennsylvania", "virginia", 
					"washington"]

states_upper = { "california": "CALIFORNIA", "michigan":"MICHIGAN", "new_york":"NEW YORK",
								"ohio":"OHIO", "pennsylvania":"PENNSYLVANIA", "virginia":"VIRGINIA",
								"washington":"WASHINGTON"} 

path = "data/"
# ignore year 2000
apples_data = { '2001':{}, '2002':{}, '2003':{}, '2004':{}, '2005':{},
								'2006':{}, '2007':{}, '2008':{}, '2009':{}, '2010': {}} 
temp_data  = {'2001':{}, '2002':{}, '2003':{}, '2004':{}, '2005':{},
							'2006':{}, '2007':{}, '2008':{}, '2009':{}, '2010':{}} 

with open(path+"apple-2000-2010.csv") as f:
	reader = csv.DictReader(f)

	for row in reader:
		#row['Period']
		#row['Value']
		if row['Period'] not in apples_data[row['Year']]:
			apples_data[row['Year']][row['Period']] = {}

		if row['Value'] == ' (NA)':
			vale = 0
		else:
			val = float(row['Value'])

		apples_data[row['Year']][row['Period']][row['State'].lower().replace(" ", "_")] = val

#print apples_data

for state in states:
	with open(path + "anual-" + state + "-2000-2010.csv") as f:
		reader = csv.DictReader(f)

		# date is formatted as YYYYmm. Ex: 200101
		# monthly mean temperature: MNTM
		for row in reader: 
			year = row["DATE"][:4]

			# ignore year 2000
			if year == '2000': continue

			month = row["DATE"][4:]

			if month == '01':
				month = "JAN"
			elif month == '02':
				month = "FEB"
			elif month == '03':
				month = "MAR"
			elif month == '04':
				month = "APR"
			elif month == '05':
				month = "MAY"
			elif month == '06':
				month = "JUN"
			elif month == '07':
				month = "JUL"
			elif month == '08':
				month = "AUG"
			elif month == '09':
				month = "SEP"
			elif month == '10':
				month = "OCT"
			elif month == '11':
				month = "NOV"
			else:
				month = "DEC"

			#print state
			if month not in temp_data[year]:
				temp_data[year][month] = {}

			if state not in temp_data[year][month]:
				temp_data[year][month][state] = []

			# watch out for -9999
			mean = float(row["MNTM"])

			# -9999 means missing data. If data is missing, get the maximun mean otherwise minimum
			if mean < 0:
				mean = float(row["MMXT"])

			# if it still -9999 use the minimum
			if mean < 0:
				mean = float(row["MMNT"])

			temp_data[year][month][state].append(mean)

# average temperature per year per month per state
avg_temps = {}
for year, months in temp_data.items():
	if year not in avg_temps:
		avg_temps[year] = {}

	for month, data in months.items():
		if month not in avg_temps[year]:
			avg_temps[year][month] = {}

		for state, sdata in data.items():
			avg_temps[year][month][state] = sum(sdata)/float(len(sdata))

# for visualization purposes print each month of each year as table
# 			state1	state2	state3 ...
# month1
# month2
ms = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
def print_as_table(data):
	for year, months in sorted(data.items()):
		print "Year", year
		print "-" * 100
		print "\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s"%tuple([st.upper() for st in states])

		for m in ms:
			print m+"\t", "%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s"%tuple([str(months[m][s]) for s in states])
		print "*"*100

def print_apples_as_table(apples_data):
	for year, months in sorted(apples_data.items()):
		print "Year", year
		print "-" * 100
		print "\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s"%tuple([st.upper() for st in states])

		for m in ms:
			vals = []
			for s in states:
				if s in months[m]:
					vals.append(str(months[m][s]))
				else:
					vals.append('0')
			print m+"\t", "%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s\t%-13s"%tuple(vals)
		print "*"*100

print "APPLES DATA"
print_apples_as_table(apples_data)
print
print_as_table(avg_temps)
