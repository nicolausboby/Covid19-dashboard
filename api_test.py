from api_covid import CovidApi

api = CovidApi()

api.fetch_data(type_data=api.CONFIRMED)

# Print data's head
api.print_data_head(type_data=api.CONFIRMED)

# Print for specific country in specific date
print(api.dfs[api.CONFIRMED]['2/1/20']['Australia'])