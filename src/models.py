class Player:
    def __init__(self, name, color):
        self._name = name
        self._color = color
        self._money = 1000
        self._position = 0

    def __str__(self):
        return (
            f"Player {self.color}: {self.name}; Saldo: {self.money}; "
            + f"Posição: {self.position}"
        )

    @property
    def name(self):
        return self._name

    @property
    def color(self):
        return self._color

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        self._money = money

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
