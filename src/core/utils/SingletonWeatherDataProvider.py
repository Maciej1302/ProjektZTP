from threading import Lock
from src.core.services.weather_data_adapter import WeatherDataAdapter


class SingletonWeatherDataProvider:
    """Singleton zarządzający instancją WeatherDataAdapter."""
    _instance = None
    _lock = Lock()  # Zapewnia bezpieczeństwo w środowisku wielowątkowym

    def __new__(cls, api_key: str = None):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    # Tworzenie instancji bez przekazywania argumentów do object.__new__
                    cls._instance = super(SingletonWeatherDataProvider, cls).__new__(cls)
                    cls._instance._initialize(api_key)  # Inicjalizacja instancji
        return cls._instance

    def _initialize(self, api_key: str):
        """Inicjalizacja Singletona."""
        if not hasattr(self, "adapter"):  # Upewnij się, że inicjalizacja jest wykonywana tylko raz
            self.adapter = WeatherDataAdapter(api_key=api_key)

    def fetch_weather(self, city: str):
        """
        Pobiera aktualne dane pogodowe za pomocą adaptera.
        """
        return self.adapter.fetch_weather(city)

    def fetch_forecast(self, city: str, days: int):
        """
        Pobiera prognozę pogody za pomocą adaptera.
        """
        return self.adapter.fetch_forecast(city, days)