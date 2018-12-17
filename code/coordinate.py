class Coordinate(object):
    """
    X and Y coordinate of a house on a map
    """

    def __init__(self):
        self.coordinate = []

    def add(self, id, x_random, y_random):
        self.coordinate.append(id)
        self.coordinate.append(x_random)
        self.coordinate.append(y_random)

    def __str__(self):
        return(f"{self.coordinate}")
