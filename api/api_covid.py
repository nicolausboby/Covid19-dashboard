# Libraries
import pandas as pd
from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2, country_name_to_country_alpha3

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

	CONTINENTS = {
    'NA': 'North America',
    'SA': 'South America', 
    'AS': 'Asia',
    'OC': 'Australia',
    'AF': 'Africa',
    'EU': 'Europe'
}

	# Variables
	dfs = {}

	def __init__(self):
		print("API Class initiated!")

	def reset_data(self):
		self.dfs = {}

	def fetch_data(self, type_data):
		print("Fetching data for", type_data)
		df = pd.read_csv(self.URL[type_data])

		# Remove unneeded Lat and Long columns
		df = df.drop(['Lat', "Long"], axis=1)

		# Group by country (some countries are divided by region)
		df = df.groupby(['Country/Region']).sum()

		df_data = []

		for index, rows in df.iterrows():
			# Rough fix for None iso-alpha cases
			if index in ["Diamond Princess", "Holy See", "MS Zaandam"]: # Obsecure countries
				continue

			if index == 'Burma': # Burma == Myanmar
				country_name = 'Myanmar'
				iso_alpha2 = 'MM'
				iso_alpha3 = 'MMR'
			elif index == "Congo (Brazzaville)":
				country_name = "Republic of the Congo"
				iso_alpha2 = 'CG'
				iso_alpha3 = 'COG'
			elif index == "Congo (Kinshasa)":
				country_name = "Democratic Republic of the Congo"
				iso_alpha2 = 'CD'
				iso_alpha3 = 'COD'
			elif index == "Cote d'Ivoire":
				country_name = index
				iso_alpha2 = 'CI'
				iso_alpha3 = 'CIV'
			elif index == 'Korea, South':
				country_name = 'South Korea'
				iso_alpha2 = 'KR'
				iso_alpha3 = 'KOR'
			elif index == 'Kosovo':
				country_name = index
				iso_alpha2 = 'XK'
				iso_alpha3 = 'XKX'
			elif index == 'Laos':
				country_name = index
				iso_alpha2 = 'LA'
				iso_alpha3 = 'LAO'
			elif index == 'Taiwan*':
				country_name = 'Taiwan'
				iso_alpha2 = 'TW'
				iso_alpha3 = 'TWN'
			elif index == 'US':
				country_name = 'United States of America'
				iso_alpha2 = 'US'
				iso_alpha3 = 'USA'
			elif index == 'Vietnam':
				iso_alpha2 = 'VN'
				iso_alpha3 = 'VNM'
			elif index == 'West Bank and Gaza':
				country_name = 'Palestine'
				iso_alpha2 = 'PS'
				iso_alpha3 = 'PSE'
			else:
				country_name = index
				iso_alpha2 = country_name_to_country_alpha2(index, cn_name_format="default")
				iso_alpha3 = country_name_to_country_alpha3(index, cn_name_format="default")

			for date, num in rows.items():
				try:
					df_data.append({
							'country': country_name,
							'continent': self.CONTINENTS[country_alpha2_to_continent_code(iso_alpha2)],
							'iso_alpha2': iso_alpha2,
							'iso_alpha3': iso_alpha3,
							'date': date,
							type_data: num
					})
				except:
					continue

		df_new = pd.DataFrame(df_data)
		df_new['date'] = pd.to_datetime(df_new['date'], format='%m/%d/%y')
		df_new['date'] = df_new['date'].astype(str)

		self.dfs[type_data] = df_new

	def get_data_df(self, type_data):
		return self.dfs[type_data]

	def get_data_dict(self, type_data):
		return self.dfs[type_data].to_dict()

	def print_data_head(self, type_data):
		print(self.dfs[type_data].head())

