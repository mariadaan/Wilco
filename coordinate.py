class Coordinate(object):
    """
    X en Y coordinaat van Woning
    """

    def __init__(self):
        """
        Lijst van x en y coordinaten
        """
        self.coordinate = []

    def add(self, id, x_random, y_random):
        self.coordinate.append(id)
        self.coordinate.append(x_random)
        self.coordinate.append(y_random)

    def __str__(self):
        return(f"{self.coordinate}")
