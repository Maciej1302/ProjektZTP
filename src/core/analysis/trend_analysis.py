from typing import List
from src.core.weather.weather_data import WeatherData
from src.core.analysis.analysis_report import AnalysisReport
from src.core.analysis.analysis_strategy import AnalysisStrategy


class TrendAnalysis(AnalysisStrategy):
    """
    Klasa realizująca analizę trendów na danych pogodowych.
    """

    def analyze(self, data: List[WeatherData]) -> AnalysisReport:
        report = AnalysisReport()
        report.summary = "Trend Analysis Report"

        # Analiza trendów: obliczanie średniej temperatury
        average_temperature = sum(d.temperature for d in data) / len(data)
        trend_details = {
            "start_date": data[0].date,
            "end_date": data[-1].date,
            "average_temperature": average_temperature
        }

        report.details = trend_details
        return report
