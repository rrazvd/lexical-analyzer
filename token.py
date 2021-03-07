class Token():
    def __init__(self, name, attribute):
        self.__name = name
        self.__attribute = attribute

    def to_string(self):
        return '<'+self.__name+','+str(self.__attribute)+'>'

    def get_name(self):
        return self.__name

    def get_attribute(self):
        return self.__attribute
