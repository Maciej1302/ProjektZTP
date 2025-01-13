from typing import List, Dict
from src.core.weather.weather_data import WeatherData
from src.core.analysis.analysis_report import AnalysisReport
from src.core.analysis.analysis_strategy import AnalysisStrategy


class TrendAnalysis(AnalysisStrategy):
    """
    Implementacja strategii analizy trendów pogodowych.
    """

    def analyze(self, data: List[WeatherData]) -> dict[str, list[float]]:
        """
        Przetwarza dane pogodowe i generuje dane wejściowe dla raportu trendów.
        """

        return {
            "temperatures": [day.temperature for day in data],
            "precipitations": [day.precipitation for day in data],
            "wind_speeds": [day.wind_speed for day in data],
        }