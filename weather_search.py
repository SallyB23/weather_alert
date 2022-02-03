import requests
import os

OWM_API_KEY = os.environ.get("OWM_API_KEY")
MY_LAT = os.environ.get("MY_LAT")
MY_LON = os.environ.get("MY_LON")


class WeatherSearch:
    def __init__(self):
        self.weather_data = None
        self.alert_event_list = []
        self.alert_description_list = []
        self.forecast_data = {}

    def search_weather(self):
        parameters = {
            "lat": MY_LAT,
            "lon": MY_LON,
            "exclude": "current,minutely, daily, hourly",
            "units": "imperial",
            "appid": OWM_API_KEY,
        }

        response = requests.get(url="http://api.openweathermap.org/data/2.5/onecall", params=parameters)
        response.raise_for_status()
        self.weather_data = response.json()
        return self.weather_data

    def get_weather_data(self):
        self.search_weather()

        self.forecast_data = {
            "weather": self.weather_data["daily"][0]["weather"][0]["description"],
            "day_temp": round((self.weather_data["daily"][0]["temp"]["day"] - 32) * 5 / 9, 1),
            "night_temp": round((self.weather_data["daily"][0]["temp"]["night"] - 32) * 5 / 9, 1),
            "day_temp_feels_like": round((self.weather_data["daily"][0]["feels_like"]["day"] - 32) * 5 / 9, 1),
            "uv": round(self.weather_data["daily"][0]["uvi"]),
            "wind_speed": round(self.weather_data["daily"][0]["wind_speed"]),
            "wind_gusts": round(self.weather_data["daily"][0]["wind_gust"]),
        }
        return self.forecast_data

    def check_alerts(self):
        for n in range(0, 2):
            try:
                self.alert_event_list.append(self.weather_data["alerts"][n]["event"])
            except KeyError:
                pass
            else:
                self.alert_description_list.append(self.weather_data["alerts"][n]["description"])

    def check_thunder(self):
        thunder_weather_ids = [(self.weather_data["hourly"][n]["weather"][0]["id"]) for n in range(0, 24)
                               if 200 <= (self.weather_data["hourly"][n]["weather"][0]["id"]) < 300]
        return len(thunder_weather_ids)

    def check_snow(self):
        snow_weather_ids = [(self.weather_data["hourly"][n]["weather"][0]["id"]) for n in range(0, 24)
                            if 600 <= (self.weather_data["hourly"][n]["weather"][0]["id"]) < 700]
        return len(snow_weather_ids)
