import requests
import settings

def weather_by_city(city_name:str) -> str:
	weather_url = "http://api.worldweatheronline.com/premium/v1/weather.ashx"
	params = {
		"key":settings.API_Key,
		"q": city_name,
		"format":"json",
		"num_of_days": 1,
		"lang": "ru"
	}
	result = requests.get(weather_url,params=params)
	

	weather = result.json()
	print(weather)
	if 'data' in weather:
		if 'current_condition' in weather['data']:
			try:
				return weather['data']['current_condition'][0]
			except(IndexError, TypeError):
				return False
	return False


	return result

if __name__ == "__main__":
	weather = weather_by_city("Bryansk,Russia")
	print(weather)