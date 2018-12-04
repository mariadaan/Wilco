class Water(object):
    """
    Water is a rectangular region representing water bodies.
    """
    def __init__(self, type_water, map):
        self.type_water = type_water
        self.map = map

    def fill_water(self, number_water):
        """
        Fills the requested area on the map with water
        """
        # determine the volume of the water bodies
        self.volume = self.width * self.height * 0.2/number_water

        # generate a random width and height (between 1 and 4)
        i = random.randint(1,4)
        self.width = int(sqrt(self.volume/i))
        self.height = self.width * i

        placed = False

        # get a random position (upper left corner of waterbody)
        while not placed:
            self.x, self.y = self.map.get_random_position()

            # check if the area is empty and save the outcome plus
            # the checked area
            if self.x + self.width <= self.width and \
                    self.y + self.height <= self.height:
                area_water_empty, area_water = \
                    self.map.is_area_water_empty(self)

                # fill subarea and save the position
                if area_water_empty:
                    area_water[:,:] = self.type_water
                    placed = True
