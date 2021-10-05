from flask import Flask
from weather import weather_by_city

# Простейшее Flask приложение

app = Flask(__name__)

@app.route('/')
def index() -> str:
	weather = weather_by_city("Moskow,Russia")
	if weather:
		return f'''сейчас {weather['temp_C']},
		 ощущается как {weather['FeelsLikeC']}'''
	else:
		return "Прогноз сейчас не доступен" 

if __name__ == "__main__":
	app.run(debug=True)
