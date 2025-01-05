import json
from typing import List
from src.core.commands.command import Command
from src.core.weather.weather_data import WeatherData


class ImportWeatherDataCommand(Command):
    """
    Konkretna implementacja polecenia importu danych pogodowych.
    """

    def __init__(self, storage: List[WeatherData]):
        """
        Inicjalizacja polecenia z magazynem danych pogodowych.

        :param storage: Lista do przechowywania zaimportowanych danych.
        """
        self.storage = storage

    def execute(self, file_path: str) -> None:
        """
        Wykonuje polecenie importu danych pogodowych z pliku JSON.

        :param file_path: Ścieżka do pliku z danymi pogodowymi.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for record in data:
                weather_data = WeatherData(
                    temperature=record["temperature"],
                    humidity=record["humidity"],
                    precipitation=record["precipitation"],
                    wind_speed=record["wind_speed"],
                    date=record["date"],
                )
                self.storage.append(weather_data)

            print(f"Zaimportowano {len(data)} rekordów pogodowych z pliku {file_path}.")

        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {file_path}.")
        except json.JSONDecodeError:
            print(f"Błąd: Plik {file_path} nie zawiera poprawnych danych JSON.")
        except KeyError as e:
            print(f"Błąd: Brakuje klucza {e} w rekordach pliku {file_path}.")
