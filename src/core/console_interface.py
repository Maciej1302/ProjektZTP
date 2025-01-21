import os
import csv
from src.core.alerts.weather_alert import StormAlert, FrostAlert
from src.core.analysis.comparison_analysis import ComparisonAnalysis
from src.core.locations.location_hierarchy import City, Region, ILocation
from src.core.analysis.report_director import ReportDirector
from src.core.analysis.analysis_report_builder import TrendAnalysisReportBuilder, ComparisonAnalysisReportBuilder
from src.core.services.weather_data_adapter import WeatherDataAdapter
from src.core.user.user import User
from src.core.alerts.weather_alert import StormAlert,FrostAlert
from src.core.analysis.trend_analysis import TrendAnalysis
from src.core.weather.weather_data import WeatherData
from src.core.utils.SingletonWeatherDataProvider import SingletonWeatherDataProvider


class ConsoleInterface:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.weatherdata = WeatherData(temperature=15, humidity=80, wind_speed=5, precipitation=2, date="2023-12-31")
        self.weather_provider = SingletonWeatherDataProvider(api_key=api_key)
        self.locations = {}
        self.adapter = WeatherDataAdapter(api_key=api_key)
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
            print("6. Wyjście")

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

            if isinstance(location, City):
                # Dla pojedynczego miasta
                city_name = location.get_name()
                weather = self.weather_provider.fetch_weather(city_name)

                # Aktualizacja danych pogodowych i powiadamianie obserwatorów
                self.weatherdata.update_weather(
                    temperature=weather.temperature,
                    humidity=weather.humidity,
                    wind_speed=weather.wind_speed,
                    precipitation=weather.precipitation,
                    date=weather.date
                )

                # Wyświetlanie danych pogodowych
                print(f"Aktualna pogoda dla {city_name}:")
                print(f"  Temperatura: {self.weatherdata.temperature:.1f}°C")

                print(f"  Wilgotność: {self.weatherdata.humidity:.1f}%")

                print(f"  Prędkość wiatru: {self.weatherdata.wind_speed:.1f} km/h")

                print(f"  Opady: {self.weatherdata.precipitation:.1f} mm")


            elif isinstance(location, Region):

                # Dla regionu – wykorzystanie get_weather do agregacji danych

                weather = location.get_weather(self.weather_provider.adapter)

                # Aktualizacja danych pogodowych w `WeatherData` (powiadamianie obserwatorów)

                self.weatherdata.update_weather(

                    temperature=weather.temperature,

                    humidity=weather.humidity,

                    wind_speed=weather.wind_speed,

                    precipitation=weather.precipitation,

                    date=weather.date

                )

                # Wyświetlanie danych pogodowych dla regionu

                print(f"Aktualna pogoda dla regionu {location_name}:")

                print(f"  Temperatura: {weather.temperature:.1f}°C")

                print(f"  Wilgotność: {weather.humidity:.1f}%")

                print(f"  Prędkość wiatru: {weather.wind_speed:.1f} km/h")

                print(f"  Opady: {weather.precipitation:.1f} mm")

            else:
                print("Nieznany typ lokalizacji.")
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

            if isinstance(location, City):
                # Obsługa dla miasta
                city_name = location.get_name()
                forecast = location.get_forecast(self.weather_provider.adapter, days)
                print(f"Prognoza pogody dla {city_name}:")
                for day in forecast:
                    print(f"  Data: {day.date}")
                    print(f"    Temperatura: {day.temperature:.1f}°C")
                    print(f"    Wilgotność: {day.humidity:.1f}%")
                    print(f"    Prędkość wiatru: {day.wind_speed:.1f} km/h")
                    print(f"    Opady: {day.precipitation:.1f} mm")

            elif isinstance(location, Region):
                # Obsługa dla regionu
                forecast = location.get_forecast(self.weather_provider.adapter, days)
                print(f"Prognoza pogody dla regionu {location_name}:")
                for day in forecast:
                    print(f"  Data: {day.date}")
                    print(f"    Temperatura: {day.temperature:.1f}°C")
                    print(f"    Wilgotność: {day.humidity:.1f}%")
                    print(f"    Prędkość wiatru: {day.wind_speed:.1f} km/h")
                    print(f"    Opady: {day.precipitation:.1f} mm")

            else:
                print("Nieznany typ lokalizacji.")
        else:
            print("Lokalizacja nieznaleziona.")

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
                self.weatherdata.attach(alert)
            elif alert_type == "frost":
                alert = FrostAlert(location=self.locations[location_name], alert_message=alert_message)
                self.weatherdata.attach(alert)
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
        """
        Analiza porównawcza prognoz pogodowych dla wybranych lokalizacji.
        """
        locations = input("Podaj nazwy lokalizacji oddzielone przecinkiem: ").split(',')
        selected_locations = []

        for location_name in locations:
            location_name = location_name.strip()
            if location_name in self.locations:
                selected_locations.append(self.locations[location_name])
            else:
                print(f"Lokalizacja {location_name} nieznaleziona.")

        if len(selected_locations) < 2:
            print("Wymagane są przynajmniej dwie lokalizacje do analizy porównawczej.")
            return

        # Pobranie prognoz dla każdej lokalizacji
        data = [location.get_forecast(self.adapter, 7) for location in selected_locations]

        # Analiza porównawcza
        analysis = ComparisonAnalysis()
        raw_report = analysis.analyze(data, selected_locations)

        # Budowanie raportu za pomocą buildera
        builder = ComparisonAnalysisReportBuilder()
        director = ReportDirector()
        final_report = director.construct(builder, raw_report.details)

        # Wyświetlanie raportu
        print("=== Raport porównawczy ===")
        for comparison in final_report.details:
            print(f"{comparison['comparison']}:")
            print(f"  Max Temp: {comparison['max_temperature']}")
            print(f"  Min Temp: {comparison['min_temperature']}")
            print(f"  Max Wind Speed: {comparison['max_wind_speed']}")
            print(f"  Min Wind Speed: {comparison['min_wind_speed']}")


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





if __name__ == "__main__":
    API_KEY = "e1cb2b3a3fed1c8e38a4ef4cc9b7c6ec"
    app = ConsoleInterface(api_key=API_KEY)
    app.main_menu()
