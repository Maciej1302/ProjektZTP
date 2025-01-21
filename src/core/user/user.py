from typing import List
from src.core.locations.location_hierarchy import ILocation
from src.core.alerts.weather_alert import WeatherAlert

class User:
    """
    Klasa reprezentująca użytkownika aplikacji.
    """

    def __init__(self, name: str):
        self.name = name
        self.favourite_locations: List[ILocation] = []
        self.alerts: List[WeatherAlert] = []

    def add_favourite_location(self, location: ILocation) -> None:
        """
        Dodaje lokalizację do listy ulubionych lokalizacji użytkownika.
        """
        self.favourite_locations.append(location)
        print(f"Lokalizacja {location.get_name()} została dodana do ulubionych.")

    def remove_favourite_location(self, location_name: str) -> None:
        """
        Usuwa lokalizację z listy ulubionych lokalizacji użytkownika.
        """
        for location in self.favourite_locations:
            if location.get_name() == location_name:
                self.favourite_locations.remove(location)
                print(f"Lokalizacja {location_name} została usunięta z ulubionych.")
                return
        print(f"Lokalizacja {location_name} nie została znaleziona w ulubionych.")

    def list_favourite_locations(self) -> None:
        """
        Wyświetla ulubione lokalizacje użytkownika.
        """
        if not self.favourite_locations:
            print("Brak ulubionych lokalizacji.")
        else:
            print("Ulubione lokalizacje użytkownika:")
            for location in self.favourite_locations:
                print(f"- {location.get_name()}")

    def add_alert(self, alert: WeatherAlert) -> None:
        """
        Dodaje alert pogodowy do użytkownika.
        """
        self.alerts.append(alert)
        print(f"Alert został dodany: {alert.alert_message} dla {alert.location.get_name()}.")

    def trigger_all_alerts(self) -> None:
        """
        Wywołuje wszystkie alerty pogodowe użytkownika.
        """
        if not self.alerts:
            print("Brak alertów do wywołania.")
        else:
            print("Wywoływanie alertów użytkownika:")
            for alert in self.alerts:
                print(f"{alert.alert_message} dla {alert.location.get_name()}")