from abc import ABC, abstractmethod
from src.core.analysis_report import AnalysisReport


class AnalysisReportBuilder(ABC):
    """
    Abstrakcyjna klasa reprezentująca budowniczego raportów analitycznych.
    """

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

    @abstractmethod
    def get_report(self) -> AnalysisReport:
        """
        Zwraca zbudowany raport analityczny.
        """
        pass


class ComparisonAnalysisReportBuilder(AnalysisReportBuilder):
    """
    Budowniczy raportów porównawczych.
    """

    def __init__(self):
        self.report = AnalysisReport()

    def set_summary(self, summary: str) -> None:
        self.report.summary = summary

    def set_details(self, details: dict) -> None:
        self.report.details = {
            "type": "Comparison",
            **details
        }

    def get_report(self) -> AnalysisReport:
        return self.report


class TrendAnalysisReportBuilder(AnalysisReportBuilder):
    """
    Budowniczy raportów trendów.
    """

    def __init__(self):
        self.report = AnalysisReport()

    def set_summary(self, summary: str) -> None:
        self.report.summary = summary

    def set_details(self, details: dict) -> None:
        self.report.details = {
            "type": "Trend",
            **details
        }

    def get_report(self) -> AnalysisReport:
        return self.report

if __name__ == "__main__":
    # Testowanie ComparisonAnalysisReportBuilder
    comparison_builder = ComparisonAnalysisReportBuilder()
    comparison_builder.set_summary("Raport porównawczy")
    comparison_builder.set_details({"location1": "Warsaw", "location2": "Krakow", "comparison_metric": "temperature"})
    comparison_report = comparison_builder.get_report()
    print(comparison_report)

    # Testowanie TrendAnalysisReportBuilder
    trend_builder = TrendAnalysisReportBuilder()
    trend_builder.set_summary("Raport trendów")
    trend_builder.set_details({"location": "Warsaw", "trend_metric": "temperature", "time_range": "last_month"})
    trend_report = trend_builder.get_report()
    print(trend_report)
