# Milou van Casteren en Maria Daan en AAAAD
# minor programmeren
# Heuristieken
# Amstelhaege


# grid maken

class Grid():

    def __init__(self, lengte, breedte):
        self.lengte = lengte
        self.breedte = breedte


    def coordinaat(self):

        for y in reversed(range(self.lengte + 1)):
            for x in range(self.breedte + 1):
                if len(str(y)) == 1:
                    coordinaat = f"({x},0{y})"
                    print(coordinaat, end="")
                else:
                    coordinaat = f"({x},{y})"
                    print(coordinaat, end="")
            print()

class Huis():

    def __init__(self):
        # self.naam = naam
        self.oppervlakte = oppervlakte
        # self.vrijstand = vrijstand
        # self.prijs = pr ijs
        # self.meerwaarde = meerwaarde

    def huis(self)




if __name__ == "__main__":
    g = Grid(32, 36)
    g.coordinaat()






# Wilco
