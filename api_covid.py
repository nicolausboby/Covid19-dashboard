# Libraries
import pandas as pd
import pycountry

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

		df_data = []

		for index, rows in df.iterrows():
			for date, num in rows.items():
				df_data.append({
          'country': index,
          'iso_alpha': self.get_country_code(index),
          'date': date,
          'cases': num
	      })

		self.dfs[type_data] = pd.DataFrame(df_data)

	def get_data_df(self, type_data):
		return self.dfs[type_data]

	def get_data_dict(self, type_data):
		return self.dfs[type_data].to_dict()

	def print_data_head(self, type_data):
		print(self.dfs[type_data].head())

	# UTILS
	def get_country_code(self, name):
		for co in list(pycountry.countries):
			if name in co.name:
				return co.alpha_3
		return None

