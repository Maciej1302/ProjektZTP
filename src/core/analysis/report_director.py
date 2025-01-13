from src.core.analysis.analysis_report import AnalysisReport
from src.core.analysis.analysis_report_builder import AnalysisReportBuilder
from typing import Any


class ReportDirector:
    """
    Klasa zarządzająca budową raportów.
    """

    def construct(self, builder: AnalysisReportBuilder, details: dict) -> AnalysisReport:
        """
        Buduje raport na podstawie podanych szczegółów.
        """
        builder.set_summary("Raport trendów pogodowych")
        builder.set_details(details)
        return builder.get_report()