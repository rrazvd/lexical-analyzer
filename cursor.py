class Cursor():
    def __init__(self):
        self.__position = 0

    def get_position(self):
        return self.__position

    def get_look_ahead(self):
        return self.__position + 1

    def get_double_look_ahead(self):
        return self.__position + 2

    def forward(self):
        self.__position += 1

    def backward(self):
        self.__position -= 1

    def to_start(self):
        self.__position = 0

    def set_position(self, position):
        self.__position = position
