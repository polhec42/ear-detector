class Rectangle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_in_rectangle(self, x, y):
        if x >= self.x and x <= (self.x + self.width) and y >= self.y and y <= (self.y + self.height):
            return True
        return False
    
    @staticmethod
    def is_in_rectangles(rectangles, x, y):
        for rec in rectangles:
            if rec.is_in_rectangle(x,y):
                return True
        return False

    def __str__ (self):
        return str(self.x) + " " + str(self.y) + " " + str(self.width) + " " + str(self.height)