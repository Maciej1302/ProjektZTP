from src.core.alerts.observer import Subject, Observer

class WeatherData(Subject):
    """
    Klasa reprezentująca dane pogodowe w aplikacji, implementująca wzorzec Observer jako Subject.
    """

    def __init__(self, temperature: float, humidity: float, wind_speed: float, precipitation: float, date: str):
        super().__init__()
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.date = date
        self._observers: list[Observer] = []

    def __repr__(self):
        return (
            f"WeatherData(Temperature: {self.temperature}°C, "
            f"Humidity: {self.humidity}%, "
            f"Wind Speed: {self.wind_speed} km/h, "
            f"Precipitation: {self.precipitation} mm, "
            f"Date: {self.date})"
        )

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

    def update_weather(self, temperature: float, humidity: float, wind_speed: float, precipitation: float, date: str):
        """
        Aktualizuje dane pogodowe i powiadamia obserwatorów.
        """
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.date = date
        self.notify()
