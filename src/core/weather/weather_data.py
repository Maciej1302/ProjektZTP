class WeatherData:
    """
    Klasa reprezentująca dane pogodowe w aplikacji.
    """

    def __init__(self, temperature: float, humidity: float, wind_speed: float, precipitation: float, date: str):
        """
        Inicjalizuje obiekt WeatherData.

        :param temperature: Temperatura w stopniach Celsjusza
        :param humidity: Wilgotność w procentach
        :param wind_speed: Prędkość wiatru w km/h
        :param precipitation: Opady w mm
        :param date: Data pomiaru w formacie YYYY-MM-DD
        """
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.precipitation = precipitation
        self.date = date

    def __repr__(self):
        """
        Reprezentacja tekstowa obiektu WeatherData.

        :return: String opisujący dane pogodowe
        """
        return (
            f"WeatherData(Temperature: {self.temperature}°C, "
            f"Humidity: {self.humidity}%, "
            f"Wind Speed: {self.wind_speed} km/h, "
            f"Precipitation: {self.precipitation} mm, "
            f"Date: {self.date})"
        )

    def validate(self):
        """
        Waliduje dane pogodowe.

        :raises ValueError: Jeśli dane są poza dopuszczalnymi granicami
        """
        if not (-100 <= self.temperature <= 60):
            raise ValueError("Temperature must be between -100°C and 60°C.")
        if not (0 <= self.humidity <= 100):
            raise ValueError("Humidity must be between 0% and 100%.")
        if self.wind_speed < 0:
            raise ValueError("Wind speed cannot be negative.")
        if self.precipitation < 0:
            raise ValueError("Precipitation cannot be negative.")
