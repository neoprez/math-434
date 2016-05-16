import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import statistics as st

states = ["california", "michigan", "new_york",
					"ohio", "pennsylvania", "virginia",
					"washington"]

states_upper = { "california": "CALIFORNIA", "michigan":"MICHIGAN", "new_york":"NEW YORK",
								"ohio":"OHIO", "pennsylvania":"PENNSYLVANIA", "virginia":"VIRGINIA",
								"washington":"WASHINGTON"}


def load_apples_info():
	periods = {"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}
	path = "data/"
	apples_info = {}
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

	return apples_info

def load_state_temperatures():
	path = "data/"
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

	return state_temperatures

def get_average(data):
	return sum(data)/float(len(data))

def get_averages_per_month_across_years(data):
	state_averages = {}
	for s in data.keys():
		years = sorted(data[s].keys())
		data_for_years = []
		state_averages[s] = []
		for year in years:
			data_for_years.append(data[s][year])

		data_for_years = np.array(data_for_years)
		for i in range(12):
			state_averages[s].append(get_average(data_for_years[:,i]))

	return state_averages


def print_state_temp_as_table(data, averages_per_month):
	ms = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
	for s in data.keys():
		print "\t"*6,states_upper[s]
		print "*" * 100
		print "    \t", "\t".join(ms)
		print "_" * 100
		years = sorted(data[s].keys())
		data_for_years = []
		for year in years:
			data_year = data[s][year]
			print year+"\t", "\t".join(map(str,data_year))
		print "-" * 100
		print "AVG:\t", "\t".join(map(str,averages_per_month[s]))
		print "*" * 100

def print_as_table(state_temperatures, apples_info, monthly_state_temp_averages, monthly_state_apples_averages):
	print "^" * 43, "TEMPERATURES", "^" * 43
	print_state_temp_as_table(state_temperatures, monthly_state_temp_averages)

	print "#" * 43, "APPLE PRICES", "#" * 43
	print_state_temp_as_table(apples_info, monthly_state_apples_averages)

if __name__ == "__main__":
	state_temperatures = load_state_temperatures()
	apples_info = load_apples_info()

	monthly_state_temp_averages = get_averages_per_month_across_years(state_temperatures)
	monthly_state_apples_averages = get_averages_per_month_across_years(apples_info)

	# print_as_table(state_temperatures, apples_info, monthly_state_temp_averages, monthly_state_apples_averages)
	# # plot averages
	# plt.figure(1)
	#
	# plt.subplot(221)
	# for state in states:
	# 	plt.plot(monthly_state_temp_averages[state], label=states_upper[state])
	# plt.title("Plot of average temperatures from 2001-2010 for 7 states")
	# plt.legend(loc=2,fontsize='x-small')
	# plt.xlabel("Month")
	# plt.ylabel("Temperature")
	#
	# plt.subplot(222)
	# for state in states:
	# 	plt.plot(monthly_state_apples_averages[state], label=states_upper[state])
	# plt.title("Plot of average prices from 2001-2010 for 7 states")
	# plt.legend(loc=2,fontsize='x-small')
	# plt.xlabel("Month")
	# plt.ylabel("Price in pounds")
	#
	# plt.show()
	#
	# # calculate correlations
	# for state in states:
	# 	print state, stats.pearsonr(monthly_state_temp_averages[state], monthly_state_apples_averages[state])

	# effects of temperature on apple production
	# x-axis is temperature
	# y-axis is the apple production in pounds
	prices = []
	temps = []
	produced_or_not = []
	for state in states:
		for pdata, tdata in zip(apples_info[state].values(), state_temperatures[state].values()):
			for price, temp in zip(pdata, tdata):
				if price > 0:
					prices.append(price)
					temps.append(temp)
					plt.scatter(temp, price, c='r')
					produced_or_not.append((temp,1))
				else:
					produced_or_not.append((temp,0))

	result = stats.linregress(temps, prices)
	correlation = st.correlation(prices, temps)
	print "Correlation: ", correlation
	# print temps
	plt.title("Effects of temperature on apple production")
	# plt.xlabel("Price in pounds")
	# plt.ylabel("Temperature")
	plt.xlabel("Temperature")
	plt.ylabel("Price in Pounds")
	plt.show()

	plt.title("Graph of temperature on production or not")
	xs, ys = zip(*produced_or_not)
	plt.scatter(xs, ys)
	plt.xlabel("Temperature")
	plt.ylabel("Produced or Not")
	plt.show()
