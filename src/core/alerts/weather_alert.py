from abc import ABC, abstractmethod
from src.core.locations.location_hierarchy import ILocation


class WeatherAlert(ABC):
    """
    Abstrakcyjna klasa reprezentująca alert pogodowy.
    """

    def __init__(self, location: ILocation, alert_message: str):
        self.location = location
        self._alert_message = alert_message

    @abstractmethod
    def trigger_alert(self) -> None:
        """
        Wywołuje alert pogodowy.
        """
        pass

    def get_alert_message(self) -> str:
        """
        Zwraca treść alertu.
        """
        return self._alert_message


class StormAlert(WeatherAlert):
    def trigger_alert(self, adapter) -> None:
        weather = self.location.get_weather(adapter)
        if weather.wind_speed > 20:
            print(f"ALERT: Burza w lokalizacji {self.location.get_name()}! {self._alert_message}")


class FrostAlert(WeatherAlert):
    def trigger_alert(self, adapter) -> None:
        weather = self.location.get_weather(adapter)
        if weather.temperature < 0:
            print(f"ALERT: Przymrozki w lokalizacji {self.location.get_name()}! {self._alert_message}")

class AlertFactory:
    """
    Fabryka alertów pogodowych.
    """

    @staticmethod
    def create_alert(alert_type: str, location: ILocation, alert_message: str):
        """
        Tworzy obiekt alertu na podstawie typu.

        :param alert_type: Typ alertu ('storm' lub 'frost')
        :param location: Lokalizacja, dla której tworzony jest alert
        :param alert_message: Treść wiadomości alertu
        :return: Obiekt typu StormAlert lub FrostAlert
        """
        if alert_type == "storm":
            return StormAlert(location=location, alert_message=alert_message)
        elif alert_type == "frost":
            return FrostAlert(location=location, alert_message=alert_message)
        else:
            raise ValueError(f"Nieznany typ alertu: {alert_type}")


if __name__ == "__main__":
    from src.core.locations.location_hierarchy import City
    from src.services.weather_data_adapter import WeatherDataAdapter

    # Inicjalizacja adaptera z kluczem API
    API_KEY = "e1cb2b3a3fed1c8e38a4ef4cc9b7c6ec"  # Wprowadź swój klucz API
    adapter = WeatherDataAdapter(api_key=API_KEY)

    # Tworzenie przykładowej lokalizacji
    warsaw = City("Warsaw", latitude=52.2297, longitude=21.0122)

    # Użycie AlertFactory do tworzenia alertów
    print("Testowanie AlertFactory:")
    try:
        storm_alert = AlertFactory.create_alert("storm", warsaw, "Silny wiatr!")
        frost_alert = AlertFactory.create_alert("frost", warsaw, "Mróz!")

        # Wywoływanie alertów z przekazaniem adaptera
        print("\nTestowanie alertów pogodowych:")
        storm_alert.trigger_alert(adapter)
        frost_alert.trigger_alert(adapter)
    except Exception as e:
        print(f"Błąd podczas testowania alertów: {e}")