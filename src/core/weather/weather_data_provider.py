from src.core.utils.multiton import Multiton
from src.services.weather_data_adapter import WeatherDataAdapter
from src.core.weather.weather_data import WeatherData


class WeatherDataProvider(Multiton):
    """
    Klasa dostarczająca dane pogodowe dla różnych lokalizacji, implementująca wzorzec Multiton.
    """

    def __init__(self, key: str):
        """
        Inicjalizacja instancji WeatherDataProvider dla konkretnej lokalizacji.
        :param key: Nazwa lokalizacji
        """
        super().__init__(key)  # Wywołanie konstruktora Multiton
        self.location = key
        self.adapter = None

    def set_adapter(self, adapter: WeatherDataAdapter):
        """
        Ustawia adapter do pobierania danych pogodowych.
        :param adapter: Obiekt adaptera
        """
        self.adapter = adapter

    def get_weather(self) -> WeatherData:
        """
        Pobiera aktualne dane pogodowe dla lokalizacji.
        :return: Obiekt WeatherData
        """
        if not self.adapter:
            raise ValueError("Adapter nie został ustawiony!")
        return self.adapter.fetch_weather(self.location)
