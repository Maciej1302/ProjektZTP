from abc import ABC, abstractmethod

class Observer(ABC):
    """
    Interfejs dla wszystkich obserwatorów (np. alerty pogodowe).
    """

    @abstractmethod
    def update(self, weather_data: dict) -> None:
        """
        Metoda aktualizująca dane obserwatora na podstawie zmian w Subject.
        :param weather_data: Słownik z danymi pogodowymi.
        """
        pass


class Subject(ABC):
    """
    Interfejs dla podmiotu obserwowanego (np. WeatherDataProvider).
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Rejestruje obserwatora.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Usuwa obserwatora.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Powiadamia wszystkich zarejestrowanych obserwatorów o zmianach.
        """
        pass
