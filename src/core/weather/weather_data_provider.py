from src.core.alerts.observer import Subject, Observer
from src.core.utils.multiton import Multiton


class WeatherDataProvider(Multiton, Subject):
    """
    Klasa dostarczająca dane pogodowe, implementująca wzorzec Multiton i Observer.
    """

    def __init__(self, key: str):
        super().__init__(key)
        self._observers: list[Observer] = []
        self.weather_data = None

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self.weather_data)

    def set_weather_data(self, weather_data: dict) -> None:
        """
        Ustawia nowe dane pogodowe i powiadamia obserwatorów.
        :param weather_data: Słownik z danymi pogodowymi.
        """
        self.weather_data = weather_data
        self.notify()
