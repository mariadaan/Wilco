class Coordinate(object):
    """
    X en Y coordinaat van Woning
    """

    def __init__(self):
        """
        lijst van x en y coordinaten
        """
        self.coordinate = []

    # def add(self, x_min, x_max, y_min, y_max):
    #     """
    #     Coordinaten toevoegen aan lijst
    #     """
    #     self.coordinate.append(x_min)
    #     self.coordinate.append(x_max)
    #     self.coordinate.append(y_min)
    #     self.coordinate.append(y_max)

    def add(self, x, y):
        self.coordinate.append(x)
        self.coordinate.append(y)

    def __str__(self):
        return(f"{self.coordinate}")
