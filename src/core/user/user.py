from typing import List
from src.core.locations.location_hierarchy import ILocation


class User:
    """
    Klasa reprezentująca użytkownika aplikacji.
    """

    def __init__(self, name: str):
        self.name = name
        self.favourite_locations: List[ILocation] = []
        self.alerts = []

    def add_favourite_location(self, location: ILocation) -> None:
        """
        Dodaje lokalizację do listy ulubionych lokalizacji użytkownika.
        """
        self.favourite_locations.append(location)

    def remove_favourite_location(self, location: ILocation) -> None:
        """
        Usuwa lokalizację z listy ulubionych lokalizacji użytkownika.
        """
        self.favourite_locations.remove(location)

    def add_alert(self, alert) -> None:
        """
        Dodaje alert pogodowy do użytkownika.
        """
        self.alerts.append(alert)

    def trigger_all_alerts(self) -> None:
        """
        Wywołuje wszystkie alerty pogodowe użytkownika.
        """
        for alert in self.alerts:
            alert.trigger_alert()

if __name__ == "__main__":
    from src.core.alerts.weather_alert import WeatherAlert
    from src.core.locations.location_hierarchy import City

    class TestAlert(WeatherAlert):
        def trigger_alert(self) -> None:
            print(f"ALERT dla lokalizacji {self.location.get_name()}: {self._alert_message}")

    # Testowanie klasy User
    user = User(name="Alice")

    # Tworzenie przykładowej lokalizacji
    warsaw = City("Warsaw", latitude=52.2297, longitude=21.0122)

    # Dodawanie lokalizacji do ulubionych
    user.add_favourite_location(warsaw)
    print(f"Ulubione lokalizacje użytkownika {user.name}: {[loc.get_name() for loc in user.favourite_locations]}")

    # Dodawanie i wywoływanie alertów
    alert = TestAlert(location=warsaw, alert_message="Silne wiatry!")
    user.add_alert(alert)
    user.trigger_all_alerts()