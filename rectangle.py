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

    @staticmethod
    def overlap(first_rectangle, second_rectangle):
        overlap_width =  min(first_rectangle.x + first_rectangle.width, second_rectangle.x + second_rectangle.width) - max(first_rectangle.x, second_rectangle.x)
        overlap_height =  min(first_rectangle.y + first_rectangle.height, second_rectangle.y + second_rectangle.height) - max(first_rectangle.y, second_rectangle.y)

        if overlap_height <= 0 or overlap_width <= 0:
            return 0

        return overlap_width * overlap_height

    def area(self):
        return self.width * self.height

    def __str__ (self):
        return str(self.x) + " " + str(self.y) + " " + str(self.width) + " " + str(self.height)