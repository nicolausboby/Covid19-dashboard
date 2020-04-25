# Libraries
import pandas as pd

class CovidApi:
	# Constants
	CONFIRMED = "confirmed"
	DEATHS = "deaths"
	RECOVERED = "recovered"

	URL = {
		CONFIRMED: "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
		DEATHS: "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
		RECOVERED: "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
	}

	# Variables
	dfs = {}

	def __init__(self):
		print("API Class initiated!")

	def reset_data(self):
		self.dfs = {}

	def fetch_data(self, type_data):
		df = pd.read_csv(self.URL[type_data])

		# Remove unneeded Lat and Long columns
		df = df.drop(['Lat', "Long"], axis=1)

		# Group by country (some countries are divided by region)
		df = df.groupby(['Country/Region']).sum()

		self.dfs[type_data] = df

	def print_data_head(self, type_data):
		print(self.dfs[type_data].head())