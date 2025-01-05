from abc import ABC, abstractmethod


class Command(ABC):
    """
    Abstrakcyjna klasa dla wzorca Command.
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        """
        Wykonuje polecenie.
        """
        pass
