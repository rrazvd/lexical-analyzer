""" this class represents a cursor that moves inside the code """
class Cursor():
    def __init__(self): 
        self.__position = 0

    def get_position(self): # returns the atual cursor position
        return self.__position

    def get_look_ahead(self): # returns the next cursor position
        return self.__position + 1

    def forward(self): # sets the cursor to forward
        self.__position += 1

    def backward(self): # sets the cursor to backward
        self.__position -= 1

    def to_start(self): # sets the cursor to the beginning
        self.__position = 0

    def set_position(self, position): # sets the cursor to any position
        self.__position = position
