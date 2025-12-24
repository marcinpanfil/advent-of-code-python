class IntPoint:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return IntPoint(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __str__(self):
        return "x={} y={}".format(self.x, self.y)

    def __repr__(self):
        return "x={} y={}".format(self.x, self.y)
