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
    Budowniczy raportów trendów.
    """

    def set_summary(self, summary: str) -> None:
        self.report.summary = summary

    def set_details(self, details: dict) -> None:
        self.report.details = {
            "type": "Trend",
            **details
        }
