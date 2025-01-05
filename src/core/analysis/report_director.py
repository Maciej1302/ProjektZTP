from src.core.analysis.analysis_report_builder import AnalysisReportBuilder
from typing import Any


class ReportDirector:
    """
    Klasa zarządzająca budową raportów.
    """

    def construct(self, builder: AnalysisReportBuilder, summary: str, details: Any) -> Any:
        """
        Konstrukcja raportu z wykorzystaniem budowniczego.

        :param builder: Obiekt budowniczego raportu
        :param summary: Podsumowanie raportu
        :param details: Szczegóły raportu
        :return: Gotowy raport analityczny
        """
        builder.set_summary(summary)
        builder.set_details(details)
        return builder.get_report()
