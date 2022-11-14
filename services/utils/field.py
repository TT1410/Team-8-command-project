
class Field:
    def __init__(self, value: str):
        self.value = value

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value!r})"
