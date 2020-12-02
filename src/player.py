class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Player(metaclass=SingletonMeta):
    def __init__(self, id, name) -> None:
        self.steamid = id
        self.name = name
        self.position = list()


class Map(metaclass=SingletonMeta):
    def __init__(self, mode, name) -> None:
        self.mode = mode
        self.name = name
        self.initial_x = 0
        self.initial_y = 0
    pass
