class Player:
    def __init__(self, name):
        self._name = name
        self._money = 1000
        self._position = 0

    def __str__(self):
        return f"Player: {self.name}; Saldo: {self.money}; Posição: {self.position}"

    @property
    def name(self):
        return self._name

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
