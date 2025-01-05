from typing import List
from src.core.weather.weather_data import WeatherData
from src.core.analysis.analysis_report import AnalysisReport
from src.core.analysis.analysis_strategy import AnalysisStrategy


class ComparisonAnalysis(AnalysisStrategy):
    """
    Klasa realizująca analizę porównawczą na danych pogodowych.
    """

    def analyze(self, data: List[WeatherData]) -> AnalysisReport:
        report = AnalysisReport()
        report.summary = "Comparison Analysis Report"

        # Porównanie: największe opady i prędkość wiatru
        max_precipitation = max(data, key=lambda d: d.precipitation)
        max_wind_speed = max(data, key=lambda d: d.wind_speed)

        comparison_details = {
            "max_precipitation": {
                "value": max_precipitation.precipitation,
                "date": max_precipitation.date
            },
            "max_wind_speed": {
                "value": max_wind_speed.wind_speed,
                "date": max_wind_speed.date
            }
        }

        report.details = comparison_details
        return report
