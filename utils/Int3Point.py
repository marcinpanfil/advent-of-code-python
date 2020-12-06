class Int3Point:
    x: int
    y: int
    z: int

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.z)

    def __str__(self):
        return "x={} y={} z={}".format(self.x, self.y, self.z)

    def __repr__(self):
        return "x={} y={} z={}".format(self.x, self.y, self.z)