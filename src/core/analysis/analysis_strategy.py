from abc import ABC, abstractmethod
from typing import List
from src.core.weather.weather_data import WeatherData
from src.core.analysis.analysis_report import AnalysisReport


class AnalysisStrategy(ABC):
    """
    Abstrakcyjna klasa strategii analizy danych pogodowych.
    """

    @abstractmethod
    def analyze(self, data: List[WeatherData]) -> AnalysisReport:
        """
        Wykonuje analizę danych pogodowych i zwraca raport.
        :param data: Lista obiektów WeatherData
        :return: Obiekt AnalysisReport
        """
        pass
