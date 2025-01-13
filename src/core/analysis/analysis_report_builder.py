from abc import ABC, abstractmethod
from src.core.analysis.analysis_report import AnalysisReport


class AnalysisReportBuilder(ABC):
    """
    Abstrakcyjna klasa budowniczego raportów analitycznych.
    """

    def __init__(self):
        self.report = AnalysisReport()

    @abstractmethod
    def set_summary(self, summary: str) -> None:
        """
        Ustawia podsumowanie raportu.
        """
        pass

    @abstractmethod
    def set_details(self, details: dict) -> None:
        """
        Ustawia szczegóły raportu.
        """
        pass

    def get_report(self) -> AnalysisReport:
        """
        Zwraca zbudowany raport analityczny.
        """
        return self.report


class ComparisonAnalysisReportBuilder(AnalysisReportBuilder):
    """
    Budowniczy raportów porównawczych.
    """

    def set_summary(self, summary: str) -> None:
        self.report.summary = summary

    def set_details(self, details: dict) -> None:
        self.report.details = {
            "type": "Comparison",
            **details
        }


class TrendAnalysisReportBuilder(AnalysisReportBuilder):
    """
    Budowniczy raportów trendów pogodowych.
    """

    def set_summary(self, summary: str) -> None:
        self.report.summary = summary

    def set_details(self, details: dict) -> None:
        """
        Szczegóły zawierają analizę trendów pogodowych, np. minimalne, maksymalne i średnie wartości.
        """
        self.report.details = {
            "type": "Trend",
            "minimum_temperature": min(details["temperatures"]),
            "maximum_temperature": max(details["temperatures"]),
            "average_temperature": sum(details["temperatures"]) / len(details["temperatures"]),
            "total_precipitation": sum(details["precipitations"]),
            "average_wind_speed": sum(details["wind_speeds"]) / len(details["wind_speeds"])
        }
