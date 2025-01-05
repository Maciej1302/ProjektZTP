import json
import csv
from typing import List
from src.core.commands.command import Command
from src.core.weather.weather_data import WeatherData


class ExportWeatherDataCommand(Command):
    """
    Konkretna implementacja polecenia eksportu danych pogodowych.
    """

    def __init__(self, data: List[WeatherData]):
        """
        Inicjalizuje polecenie eksportu z listą danych pogodowych.

        :param data: Lista obiektów WeatherData do eksportu.
        """
        self.data = data

    def execute(self, file_path: str, format: str = "json") -> None:
        """
        Eksportuje dane pogodowe do pliku w określonym formacie.

        :param file_path: Ścieżka do pliku wyjściowego.
        :param format: Format pliku ("json" lub "csv").
        """
        if format.lower() == "json":
            self._export_to_json(file_path)
        elif format.lower() == "csv":
            self._export_to_csv(file_path)
        else:
            raise ValueError("Nieobsługiwany format eksportu. Dostępne formaty: 'json', 'csv'.")

    def _export_to_json(self, file_path: str) -> None:
        """
        Eksportuje dane pogodowe do pliku JSON.

        :param file_path: Ścieżka do pliku wyjściowego.
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json_data = [weather.__dict__ for weather in self.data]
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            print(f"Dane pogodowe zapisano w pliku JSON: {file_path}")
        except Exception as e:
            print(f"Błąd podczas eksportu do JSON: {e}")

    def _export_to_csv(self, file_path: str) -> None:
        """
        Eksportuje dane pogodowe do pliku CSV.

        :param file_path: Ścieżka do pliku wyjściowego.
        """
        try:
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["temperature", "humidity", "precipitation", "wind_speed", "date"])
                for weather in self.data:
                    writer.writerow([
                        weather.temperature,
                        weather.humidity,
                        weather.precipitation,
                        weather.wind_speed,
                        weather.date,
                    ])
            print(f"Dane pogodowe zapisano w pliku CSV: {file_path}")
        except Exception as e:
            print(f"Błąd podczas eksportu do CSV: {e}")
