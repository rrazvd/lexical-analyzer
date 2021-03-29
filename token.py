"""
This class represents a Token.
"""
class Token():
    def __init__(self, name, attribute, pos):
        self.__name = name
        self.__attribute = attribute
        self.__pos = pos

    def to_string(self):
        return str(self.__pos[0] + 1) + ' ' + self.__name + ' ' + str(self.__attribute)

    def get_name(self):
        return self.__name

    def get_attribute(self):
        return self.__attribute

    def get_pos(self):
        return self.__pos
