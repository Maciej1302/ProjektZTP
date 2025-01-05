from abc import ABC, abstractmethod
from typing import List
from src.services.weather_data_adapter import WeatherDataAdapter
from src.core.weather.weather_data import WeatherData


class ILocation(ABC):
    """
    Interfejs dla lokalizacji (City i Region).
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Zwraca nazwę lokalizacji.
        """
        pass

    @abstractmethod
    def get_weather(self, adapter: WeatherDataAdapter) -> WeatherData:
        """
        Pobiera dane pogodowe dla lokalizacji.

        :param adapter: Adapter do pobierania danych pogodowych.
        :return: Obiekt WeatherData z danymi pogodowymi.
        """
        pass

    @abstractmethod
    def get_forecast(self, adapter: WeatherDataAdapter, days: int) -> List[WeatherData]:
        """
        Pobiera prognozę pogody dla lokalizacji na określoną liczbę dni.

        :param adapter: Adapter do pobierania danych pogodowych.
        :param days: Liczba dni prognozy.
        :return: Lista obiektów WeatherData reprezentujących prognozę.
        """
        pass

class City(ILocation):
    """
    Klasa reprezentująca pojedyncze miasto.
    """

    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def get_name(self) -> str:
        return self.name

    def get_weather(self, adapter: WeatherDataAdapter) -> WeatherData:
        return adapter.fetch_weather(self.name)

    def get_forecast(self, adapter: WeatherDataAdapter, days: int) -> List[WeatherData]:
        return adapter.fetch_forecast(self.name, days)

class Region(ILocation):
    """
    Klasa reprezentująca region, który może zawierać miasta i inne regiony.
    """

    def __init__(self, name: str):
        self.name = name
        self.locations: List[ILocation] = []

    def get_name(self) -> str:
        return self.name

    def add_location(self, location: ILocation):
        """
        Dodaje lokalizację (City lub Region) do regionu.

        :param location: Obiekt implementujący ILocation.
        """
        self.locations.append(location)

    def remove_location(self, location: ILocation):
        """
        Usuwa lokalizację (City lub Region) z regionu.

        :param location: Obiekt implementujący ILocation.
        """
        self.locations.remove(location)

    def get_locations(self) -> List[ILocation]:
        """
        Zwraca listę lokalizacji w regionie.

        :return: Lista lokalizacji.
        """
        return self.locations

    def get_weather(self, adapter: WeatherDataAdapter) -> WeatherData:
        """
        Pobiera dane pogodowe dla regionu. Agreguje dane z podlokalizacji.

        :param adapter: Adapter do pobierania danych pogodowych.
        :return: Agregowane dane pogodowe dla regionu.
        """
        # Dla uproszczenia przyjmujemy średnią wartości dla regionu
        total_temperature = 0
        total_humidity = 0
        total_wind_speed = 0
        total_precipitation = 0
        count = 0

        for location in self.locations:
            weather = location.get_weather(adapter)
            total_temperature += weather.temperature
            total_humidity += weather.humidity
            total_wind_speed += weather.wind_speed
            total_precipitation += weather.precipitation
            count += 1

        if count == 0:
            return WeatherData(0, 0, 0, 0, "N/A")

        return WeatherData(
            temperature=total_temperature / count,
            humidity=total_humidity / count,
            wind_speed=total_wind_speed / count,
            precipitation=total_precipitation / count,
            date="Aggregated"
        )

    def get_forecast(self, adapter: WeatherDataAdapter, days: int) -> List[WeatherData]:
        """
        Pobiera prognozę pogody dla regionu na określoną liczbę dni.

        :param adapter: Adapter do pobierania danych pogodowych.
        :param days: Liczba dni prognozy.
        :return: Lista obiektów WeatherData reprezentujących prognozę.
        """
        aggregated_forecast = []

        for day in range(days):
            total_temperature = 0
            total_humidity = 0
            total_wind_speed = 0
            total_precipitation = 0
            count = 0

            for location in self.locations:
                forecast = location.get_forecast(adapter, days)
                daily_weather = forecast[day] if day < len(forecast) else None
                if daily_weather:
                    total_temperature += daily_weather.temperature
                    total_humidity += daily_weather.humidity
                    total_wind_speed += daily_weather.wind_speed
                    total_precipitation += daily_weather.precipitation
                    count += 1

            if count > 0:
                aggregated_forecast.append(WeatherData(
                    temperature=total_temperature / count,
                    humidity=total_humidity / count,
                    wind_speed=total_wind_speed / count,
                    precipitation=total_precipitation / count,
                    date=f"Day {day + 1}"
                ))

        return aggregated_forecast

if __name__ == "__main__":
    # Testowanie hierarchii lokalizacji

    # Przygotowanie adaptera z fikcyjnym kluczem API
    API_KEY = "e1cb2b3a3fed1c8e38a4ef4cc9b7c6ec"
    adapter = WeatherDataAdapter(api_key=API_KEY)

    # Tworzenie miast
    warsaw = City("Warsaw", latitude=52.2297, longitude=21.0122)
    krakow = City("Krakow", latitude=50.0647, longitude=19.9450)

    # Tworzenie regionu
    mazowsze = Region("Mazowsze")
    mazowsze.add_location(warsaw)

    # Tworzenie kraju
    poland = Region("Poland")
    poland.add_location(mazowsze)
    poland.add_location(krakow)

    # Testowanie pobierania danych pogodowych
    print("Pogoda dla Warszawy:")
    print(warsaw.get_weather(adapter))

    print("\nPogoda dla Mazowsza:")
    print(mazowsze.get_weather(adapter))

    print("\nPogoda dla Polski:")
    print(poland.get_weather(adapter))

    print("\nPrognoza dla Krakowa na 3 dni:")
    forecast = krakow.get_forecast(adapter, days=3)
    for day, weather in enumerate(forecast, start=1):
        print(f"Day {day}: {weather}")
