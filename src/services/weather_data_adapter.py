import requests
from datetime import datetime, timezone
from src.core.weather.weather_data import WeatherData

class WeatherDataAdapter:
    """
    Adapter przekształcający dane z OpenWeatherMap API na obiekt WeatherData.
    """

    API_URL = "https://api.openweathermap.org/data/2.5/weather"
    FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key: str):
        """
        Inicjalizuje adapter z kluczem API.

        :param api_key: Klucz API dla OpenWeatherMap
        """
        self.api_key = api_key

    def fetch_weather(self, city: str) -> WeatherData:
        """
        Pobiera dane pogodowe z OpenWeatherMap API i przekształca je na obiekt WeatherData.

        :param city: Nazwa miasta, dla którego pobierane są dane pogodowe
        :return: Obiekt WeatherData
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Temperatura w °C
        }

        response = requests.get(self.API_URL, params=params)
        response.raise_for_status()

        data = response.json()

        # Przekształcenie danych z JSON na WeatherData
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"] * 3.6  # m/s → km/h
        precipitation = data.get("rain", {}).get("1h", 0.0)  # Opady w mm (jeśli istnieją)
        date = datetime.fromtimestamp(data["dt"], tz=timezone.utc).strftime("%Y-%m-%d")

        return WeatherData(
            temperature=temperature,
            humidity=humidity,
            wind_speed=wind_speed,
            precipitation=precipitation,
            date=date
        )

    def fetch_forecast(self, city: str, days: int) -> list[WeatherData]:
        """
        Pobiera prognozę pogody z OpenWeatherMap API i przekształca ją na listę obiektów WeatherData.

        :param city: Nazwa miasta, dla którego pobierana jest prognoza
        :param days: Liczba dni prognozy
        :return: Lista obiektów WeatherData
        """
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric",
            "cnt": days * 8  # Prognozy co 3 godziny (8 na dzień)
        }

        response = requests.get(self.FORECAST_URL, params=params)
        response.raise_for_status()

        data = response.json()
        forecast = []

        for item in data["list"]:
            temperature = item["main"]["temp"]
            humidity = item["main"]["humidity"]
            wind_speed = item["wind"]["speed"] * 3.6
            precipitation = item.get("rain", {}).get("3h", 0.0)  # Opady na 3 godziny
            date = datetime.fromtimestamp(item["dt"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

            forecast.append(WeatherData(
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                precipitation=precipitation,
                date=date
            ))

        return forecast[:days]  # Ograniczenie wyników do liczby dni

# Przykład użycia !!!!!!do usuniecia!!!!!!
if __name__ == "__main__":
    API_KEY = "e1cb2b3a3fed1c8e38a4ef4cc9b7c6ec"  # Wprowadź swój klucz API
    adapter = WeatherDataAdapter(api_key=API_KEY)

    try:
        weather = adapter.fetch_weather("Warsaw")
        print("Pogoda teraz:", weather)

        forecast = adapter.fetch_forecast("Warsaw", 3)
        print("Prognoza na 3 dni:")
        for day, weather in enumerate(forecast, start=1):
            print(f"Dzień {day}: {weather}")
    except requests.HTTPError as e:
        print(f"Błąd pobierania danych: {e}")
