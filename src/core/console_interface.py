import os
import csv
from src.core.alerts.weather_alert import StormAlert, FrostAlert
from src.core.locations.location_hierarchy import City, Region
from src.core.analysis.report_director import ReportDirector
from src.core.analysis.analysis_report_builder import TrendAnalysisReportBuilder
from src.core.services.weather_data_adapter import WeatherDataAdapter
from src.core.user.user import User
from src.core.alerts.weather_alert import StormAlert,FrostAlert
from src.core.analysis.trend_analysis import TrendAnalysis

class ConsoleInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.adapter = WeatherDataAdapter(api_key=self.api_key)
        self.locations = {}
        self.alerts = []
        self.user = User(name='Cukierek')

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
            print("7. Zarządzanie użytkownikiem")
            print("8. Wyjście")

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
                self.manage_user()  # Zarządzanie użytkownikiem
            elif choice == "8":
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
            for alert in self.alerts:
                name = alert.location.get_name
                if name in self.locations.keys():
                    print(alert.alert_message)
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
        print("5. Dodaj miasto do regionu")


        choice = input("Wybierz opcję: ")
        if choice == "1":
            self.add_city()
        elif choice == "2":
            self.add_region()
        elif choice == "3":
            self.remove_location()
        elif choice == "4":
            self.list_locations()
        elif choice=="5":
            self.add_region_location()
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

    def add_region_location(self):
        name = input("Podaj nazwe regionu dla którego chcesz dodać miasto")
        locations = input("Podaj nazwe miasta które chcesz dodać do tego regionu ")
        self.locations[name].add_location(City(name=locations))
        print(f"Miasta {locations} zostały dodane do regionu {name}.")

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
        """
        Analiza trendów pogodowych dla wybranej lokalizacji.
        """
        location_name = input("Podaj nazwę lokalizacji: ")
        if location_name in self.locations:
            location = self.locations[location_name]
            data = location.get_forecast(self.adapter, 7)  # Pobierz prognozę na 7 dni

            # Przygotowanie danych dla analizy trendów
            trend_analysis = TrendAnalysis()
            trend_data = trend_analysis.analyze(data)

            # Tworzenie raportu z użyciem ReportDirector i TrendAnalysisReportBuilder
            builder = TrendAnalysisReportBuilder()
            director = ReportDirector()
            report = director.construct(builder, trend_data)

            # Wyświetlanie raportu
            print("=== Raport trendów ===")
            print(report)

            # Opcja zapisu raportu do pliku CSV
            save_choice = input("Czy chcesz zapisać raport w formacie CSV? (tak/nie): ").strip().lower()
            if save_choice == "tak":
                self.save_report_to_csv(report, f"trend_analysis_{location_name}.csv")
        else:
            print("Lokalizacja nieznaleziona.")

    def comparison_analysis(self):
        location1_name = input("Podaj nazwę pierwszej lokalizacji: ")
        location2_name = input("Podaj nazwę drugiej lokalizacji: ")

        if location1_name in self.locations and location2_name in self.locations:
            location1 = self.locations[location1_name]
            location2 = self.locations[location2_name]

            # Pobranie danych pogodowych dla obu lokalizacji
            data1 = location1.get_forecast(self.adapter, 7)
            data2 = location2.get_forecast(self.adapter, 7)

            # Tworzenie raportu porównawczego
            #builder = ComparisonAnalysisReportBuilder()
            director = ReportDirector()
            #report = director.construct(builder, (data1, data2))
            print("Raport porównawczy:")
            print(report)

            # Zapis raportu do pliku CSV
            save_choice = input("Czy chcesz zapisać raport w formacie CSV? (tak/nie): ").strip().lower()
            if save_choice == "tak":
                self.save_report_to_csv(report, f"comparison_analysis_{location1_name}_vs_{location2_name}.csv")
        else:
            print("Jedna lub obie lokalizacje nie zostały znalezione.")

    def save_report_to_csv(self, report, filename: str):
        """
        Zapisuje raport do pliku CSV.
        """
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Summary", "Details"])
                writer.writerow([report.summary, report.details])
            print(f"Raport został zapisany jako {filename}.")
        except Exception as e:
            print(f"Wystąpił błąd podczas zapisywania pliku: {e}")

    def import_export_data(self):
        print("Import/Eksport jeszcze niezaimplementowany.")

    def manage_user(self):
        """
        Zarządzanie użytkownikiem aplikacji.
        """
        while True:
            self.clear_screen()
            print("=== Zarządzanie użytkownikiem ===")
            print("1. Dodaj ulubioną lokalizację")
            print("2. Usuń ulubioną lokalizację")
            print("3. Wyświetl ulubione lokalizacje")
            print("4. Dodaj alert użytkownika")
            print("5. Wywołaj wszystkie alerty użytkownika")
            print("6. Powrót do menu głównego")

            choice = input("Wybierz opcję: ")
            if choice == "1":
                self.add_favourite_location()
            elif choice == "2":
                self.remove_favourite_location()
            elif choice == "3":
                self.user.list_favourite_locations()
                input("\nNaciśnij Enter, aby kontynuować.")
            elif choice == "4":
                self.add_user_alert()
            elif choice == "5":
                self.user.trigger_all_alerts()
                input("\nNaciśnij Enter, aby kontynuować.")
            elif choice == "6":
                break
            else:
                print("Nieprawidłowy wybór, spróbuj ponownie.")

    def add_favourite_location(self):
        """
        Dodaje lokalizację do ulubionych lokalizacji użytkownika.
        """
        location_name = input("Podaj nazwę lokalizacji: ")
        self.user.add_favourite_location(location_name)


    def remove_favourite_location(self):
        """
        Usuwa lokalizację z ulubionych lokalizacji użytkownika.
        """
        location_name = input("Podaj nazwę lokalizacji do usunięcia: ")
        self.user.remove_favourite_location(location_name)

    def add_user_alert(self):
        """
        Dodaje alert pogodowy do użytkownika.
        """
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
            self.user.add_alert(alert)
        else:
            print("Lokalizacja nieznaleziona.")


if __name__ == "__main__":
    API_KEY = "e1cb2b3a3fed1c8e38a4ef4cc9b7c6ec"
    app = ConsoleInterface(api_key=API_KEY)
    app.main_menu()
