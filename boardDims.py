from const import DIM

class Board_Dim:

    def __init__ (self, size, xcor, ycor):
        self.size = size
        self.sqsize = self.size // DIM
        self.xcor = xcor
        self.ycor = ycor