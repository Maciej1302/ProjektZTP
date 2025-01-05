class Multiton:
    """
    Wzorzec Multiton umożliwiający tworzenie wielu unikalnych instancji na podstawie klucza.
    """

    _instances = {}

    @classmethod
    def get_instance(cls, key):
        """
        Zwraca instancję związaną z podanym kluczem. Jeśli instancja nie istnieje, tworzy nową.

        :param key: Klucz identyfikujący instancję
        :return: Instancja klasy
        """
        if key not in cls._instances:
            cls._instances[key] = cls(key)
        return cls._instances[key]

    def __init__(self, key):
        """
        Inicjalizuje instancję Multitona.
        :param key: Klucz instancji
        """
        if key in self._instances:
            raise ValueError(f"Instancja z kluczem '{key}' już istnieje. Użyj get_instance()!")
        self.key = key
