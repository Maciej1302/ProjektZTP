class AnalysisReport:
    """
    Klasa reprezentująca raport analityczny.
    """

    def __init__(self):
        self.summary = ""
        self.details = {}

    def __str__(self):
        return f"AnalysisReport(summary='{self.summary}', details={self.details})"