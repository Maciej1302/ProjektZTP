from src.core.analysis.report_director import ReportDirector
from src.core.analysis.analysis_report_builder import ComparisonAnalysisReportBuilder, TrendAnalysisReportBuilder

if __name__ == "__main__":
    # Inicjalizacja dyrektora
    director = ReportDirector()

    # Testowanie ComparisonAnalysisReportBuilder
    comparison_builder = ComparisonAnalysisReportBuilder()
    comparison_report = director.construct(
        builder=comparison_builder,
        summary="Porównanie warunków pogodowych",
        details={"location1": "Warsaw", "location2": "Krakow", "comparison_metric": "temperature"}
    )
    print(comparison_report)

    # Testowanie TrendAnalysisReportBuilder
    trend_builder = TrendAnalysisReportBuilder()
    trend_report = director.construct(
        builder=trend_builder,
        summary="Trendy pogodowe w Warszawie",
        details={"location": "Warsaw", "trend_metric": "temperature", "time_range": "last_month"}
    )
    print(trend_report)
