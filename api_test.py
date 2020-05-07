from api_covid import CovidApi

api = CovidApi()

api.fetch_data(type_data=api.CONFIRMED)

# Print data's head
api.print_data_head(type_data=api.CONFIRMED)

# Print for specific date in specific country with DF
# print(api.get_data_df(api.CONFIRMED)['2/1/20']['Australia'])

# Print for specific date in specific country with dict
# print(api.get_data_dict(api.CONFIRMED)['2/1/20']['Australia'])