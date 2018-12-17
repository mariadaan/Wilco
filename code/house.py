class House(object):
    """
    This is the House class. In this object, all features of each house type
    are defined.
    """
    def __init__(self, id, name, length, width, price, min_space, value_increase):
        self.id = id
        self.name = name
        self.length = length
        self.width = width
        self.price = price
        self.min_space = min_space
        self.value_increase = value_increase


    def __str__(self):
        return(str(self.id) + self.name, self.length, self.width, self.price, self.min_space, self.value_increase)
