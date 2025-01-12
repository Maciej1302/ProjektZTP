import os
from src.core.alerts.weather_alert import StormAlert, FrostAlert
from src.core.locations.location_hierarchy import City, Region
from src.core.analysis.report_director import ReportDirector
from src.core.analysis.analysis_report_builder import TrendAnalysisReportBuilder
from src.core.services.weather_data_adapter import WeatherDataAdapter

class ConsoleInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.adapter = WeatherDataAdapter(api_key=self.api_key)
        self.locations = {}
        self.alerts = []

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def main_menu(self):
        while True:
            self.clear_screen()
            print("===== Aplikacja Pogodowa =====")
            print("1. Przegląd aktualnych warunków pogodowych")
            print("2. Prognozy pogody")
            print("3. Zarządzanie lokalizacjami")
            print("4. Alerty pogodowe")
            print("5. Analizy i raporty pogodowe")
            print("6. Import/eksport danych")
            print("7. Wyjście")

            choice = input("Wybierz opcję: ")
            if choice == "1":
                self.view_current_weather()
            elif choice == "2":
                self.view_forecasts()
            elif choice == "3":
                self.manage_locations()
            elif choice == "4":
                self.manage_alerts()
            elif choice == "5":
                self.weather_analysis_reports()
            elif choice == "6":
                self.import_export_data()
            elif choice == "7":
                print("Do zobaczenia!")
                break
            else:
                print("Nieprawidłowy wybór, spróbuj ponownie.")

    def view_current_weather(self):
        self.clear_screen()
        print("=== Przegląd aktualnych warunków pogodowych ===")
        location_name = input("Podaj nazwę lokalizacji (miasto lub region): ")
        if location_name in self.locations:
            location = self.locations[location_name]
            weather = location.get_weather(self.adapter)
            print(f"Aktualna pogoda dla {location_name}:")
            print(weather)
        else:
            print("Lokalizacja nieznaleziona.")
        input("\nNaciśnij Enter, aby powrócić do menu.")

    def view_forecasts(self):
        self.clear_screen()
        print("=== Prognozy pogody ===")
        location_name = input("Podaj nazwę lokalizacji (miasto lub region): ")
        if location_name in self.locations:
            location = self.locations[location_name]
            days = int(input("Podaj liczbę dni prognozy (3 lub 7): "))
            forecast = location.get_forecast(self.adapter, days)
            print(f"Prognoza pogody dla {location_name}:")
            for day in forecast:
                print(day)
        else:
            print("Lokalizacja nieznaleziona.")
        input("\nNaciśnij Enter, aby powrócić do menu.")

    def manage_locations(self):
        self.clear_screen()
        print("=== Zarządzanie lokalizacjami ===")
        print("1. Dodaj miasto")
        print("2. Dodaj region")
        print("3. Usuń lokalizację")
        print("4. Wyświetl wszystkie lokalizacje")

        choice = input("Wybierz opcję: ")
        if choice == "1":
            self.add_city()
        elif choice == "2":
            self.add_region()
        elif choice == "3":
            self.remove_location()
        elif choice == "4":
            self.list_locations()
        else:
            print("Nieprawidłowy wybór.")

    def add_city(self):
        name = input("Podaj nazwę miasta: ")
        self.locations[name] = City(name=name)
        print(f"Miasto {name} zostało dodane.")

    def add_region(self):
        name = input("Podaj nazwę regionu: ")
        self.locations[name] = Region(name=name)
        print(f"Region {name} został dodany.")

    def remove_location(self):
        name = input("Podaj nazwę lokalizacji do usunięcia: ")
        if name in self.locations:
            del self.locations[name]
            print(f"Lokalizacja {name} została usunięta.")
        else:
            print("Lokalizacja nieznaleziona.")

    def list_locations(self):
        print("Lista lokalizacji:")
        for name in self.locations:
            print(f"- {name}")

    def manage_alerts(self):
        self.clear_screen()
        print("=== Zarządzanie alertami pogodowymi ===")
        print("1. Dodaj alert")
        print("2. Wyświetl wszystkie alerty")

        choice = input("Wybierz opcję: ")
        if choice == "1":
            self.add_alert()
        elif choice == "2":
            self.list_alerts()
        else:
            print("Nieprawidłowy wybór.")

    def add_alert(self):
        location_name = input("Podaj nazwę lokalizacji: ")
        if location_name in self.locations:
            alert_type = input("Podaj typ alertu (storm/frost): ")
            alert_message = input("Podaj treść alertu: ")
            if alert_type == "storm":
                alert = StormAlert(location=self.locations[location_name], alert_message=alert_message)
            elif alert_type == "frost":
                alert = FrostAlert(location=self.locations[location_name], alert_message=alert_message)
            else:
                print("Nieprawidłowy typ alertu.")
                return
            self.alerts.append(alert)
            print("Alert został dodany.")
        else:
            print("Lokalizacja nieznaleziona.")

    def list_alerts(self):
        print("Lista alertów:")
        for alert in self.alerts:
            print(f"- {alert.alert_message} dla {alert.location.get_name()}")

    def weather_analysis_reports(self):
        self.clear_screen()
        print("=== Analizy i raporty pogodowe ===")
        print("1. Analiza trendów")
        print("2. Analiza porównawcza")

        choice = input("Wybierz opcję: ")
        if choice == "1":
            self.trend_analysis()
        elif choice == "2":
            self.comparison_analysis()
        else:
            print("Nieprawidłowy wybór.")

    def trend_analysis(self):
        location_name = input("Podaj nazwę lokalizacji: ")
        if location_name in self.locations:
            location = self.locations[location_name]
            data = location.get_forecast(self.adapter, 7)
            builder = TrendAnalysisReportBuilder()
            director = ReportDirector()
            report = director.construct(builder, data)
            print("Raport trendów:")
            print(report)
        else:
            print("Lokalizacja nieznaleziona.")

    def comparison_analysis(self):
        print("Analiza porównawcza jeszcze niezaimplementowana.")

    def import_export_data(self):
        print("Import/Eksport jeszcze niezaimplementowany.")


if __name__ == "__main__":
    API_KEY = "e1cb2b3a3fed1c8e38a4ef4cc9b7c6ec"
    app = ConsoleInterface(api_key=API_KEY)
    app.main_menu()
