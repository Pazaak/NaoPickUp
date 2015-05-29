__author__ = 'maleza'


class Robot():
    def __init__(self, x_, y_, dir_):
        self.x = x_
        self.y = y_
        self.dir = dir_

    def __str__(self):
        return "I'm "+self.dir+" in ("+str(self.x)+", "+str(self.y)+")"


class Object():
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def toMessage(self):
        return str(self.x)+" "+str(self.y)+" "