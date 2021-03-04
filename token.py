class Token():
    def __init__(self, name, attribute):
        self.name = name
        self.attribute = attribute

    def to_string(self):
        return '<'+self.name+','+str(self.attribute)+'>'
