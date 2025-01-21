from typing import List

from src.core.locations.location_hierarchy import ILocation
from src.core.weather.weather_data import WeatherData
from src.core.analysis.analysis_report import AnalysisReport
from src.core.analysis.analysis_strategy import AnalysisStrategy


class ComparisonAnalysis(AnalysisStrategy):
    """
    Klasa implementująca analizę porównawczą.
    """

    def analyze(self, data: List[List[WeatherData]], locations: List[ILocation]) -> AnalysisReport:
        report = AnalysisReport()
        report.summary = "Comparison Analysis Report"

        details = []
        for idx, forecast in enumerate(data):
            max_temp = max(day.temperature for day in forecast)
            min_temp = min(day.temperature for day in forecast)
            max_wind = max(day.wind_speed for day in forecast)
            min_wind = min(day.wind_speed for day in forecast)

            # Pobieramy nazwę lokalizacji z przekazanych obiektów `locations`
            city_name = locations[idx].get_name()

            details.append({
                "city": city_name,
                "max_temperature": max_temp,
                "min_temperature": min_temp,
                "max_wind_speed": max_wind,
                "min_wind_speed": min_wind,
            })

        report.details = details
        return report
