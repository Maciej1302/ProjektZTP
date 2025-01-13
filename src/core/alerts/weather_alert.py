from src.core.alerts.observer import Observer
from src.core.locations.location_hierarchy import ILocation


class WeatherAlert(Observer):
    """
    Abstrakcyjna klasa reprezentująca alert pogodowy.
    """

    def __init__(self, location: ILocation, alert_message: str):
        self.location = location
        self.alert_message = alert_message

    def update(self, weather_data: dict) -> None:
        """
        Wywołuje logikę alertu na podstawie nowych danych pogodowych.
        :param weather_data: Słownik z danymi pogodowymi.
        """
        self.trigger_alert(weather_data)

    def trigger_alert(self, weather_data: dict) -> None:
        """
        Abstrakcyjna metoda wyzwalająca alert.
        """
        pass


class StormAlert(WeatherAlert):
    def trigger_alert(self, weather_data: dict) -> None:
        if weather_data["wind_speed"] > 10:
            print(f"ALERT: {self.alert_message} w lokalizacji {self.location.get_name()}!")


class FrostAlert(WeatherAlert):
    def trigger_alert(self, weather_data: dict) -> None:
        if weather_data["temperature"] < 0:
            print(f"ALERT: {self.alert_message} w lokalizacji {self.location.get_name()}!")
