from coordinate import Coordinate

class Uniek(object):
    def __init__(self, id):
        self.id = id
        self.coordinate = Coordinate()

    def __str__(self):
        return(str(self.id, self.coordinate))
