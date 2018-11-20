# Milou van Casteren en Maria Daan en AAAAD
# minor programmeren
# Heuristieken
# Amstelhaege

from woning import Woning
import numpy as np
import matplotlib.pyplot as plt
import random as rd

GRID_LEN = 321
GRID_BRE = 361

class Amstelhaege():
    def __init__(self):
        self.woningen = self.load_woningen("woningen.txt")
        self.make_grid = self.make_grid()
        self.count = 0
        self.xcoordinaat_lijst = []
        self.ycoordinaat_lijst = []

    def load_woningen(self, filename):
        with open(filename, "r") as f:
            content = f.readlines()
            # remove whitespace characters like `\n` at the end of each line.
            f = [x.strip() for x in content]
            woningen = []
            itemnr = 0
            for item in f:
                # voeg elk type woning toe aan lijst
                if item == "~":
                    id = f[itemnr + 1]
                    naam = f[itemnr + 2]
                    lengte = float(f[itemnr + 3])
                    breedte = float(f[itemnr + 4])
                    prijs = float(f[itemnr + 5])
                    minvrijstand = float(f[itemnr + 6])
                    waardestijging = float(f[itemnr + 7])
                    woning = Woning(id, naam, lengte, breedte, prijs, minvrijstand, waardestijging)
                    woningen.append(woning)
                    itemnr += 1
                else:
                    itemnr += 1
        return woningen

    def make_grid(self):
        x = np.arange(0, GRID_LEN)
        y = np.arange(0, GRID_BRE)
        x_mesh, y_mesh = np.meshgrid(x,y)
        plt.scatter(x_mesh, y_mesh)

    # def huizenvariant_20():
    #     eengezins_20 = 12
    #     bungalows_20 = 5
    #     villas_20 = 3
    #     combinatie_woningen = []

    def build_house(self, id, x_random, y_random):
        woning = self.woningen[id - 1]
        len = woning.lengte
        bre = woning.breedte
        VRIJSTAND = woning.minvrijstand

        self.xcoordinaat_lijst.append(x_random)
        self.ycoordinaat_lijst.append(y_random)

        x1 = np.arange(x_random, (int(bre * 2) + x_random))
#            print(x1)
        y1 = np.arange(y_random, (int(len * 2) + y_random))
#            print(y1)

        x2 = np.arange((x_random - VRIJSTAND), ((int(bre * 2) + x_random) + VRIJSTAND))
        y2 = np.arange((y_random - VRIJSTAND), ((int(len * 2) + y_random) + VRIJSTAND))

        x1_mesh, y1_mesh = np.meshgrid(x1,y1)
        x2_mesh, y2_mesh = np.meshgrid(x2,y2)
        plt.scatter(x2_mesh, y2_mesh)
        plt.scatter(x1_mesh, y1_mesh)

        self.count += 1

        if self.count < 5:
            self.place(id)



    def check_place(self, id, x_random, y_random):
        woning = self.woningen[id - 1]
        len = int(woning.lengte)
        bre = int(woning.breedte)

        # if len(self.xcoordinaat_lijst) > 0:
        for coordinate in self.xcoordinaat_lijst:
            coordinate = int(coordinate)
            for x in range(coordinate, (coordinate + len)):
                if x == x_random:
                    self.place(id)
            for x in range(coordinate, (coordinate - len)):
                if x == x_random:
                    self.place(id)
        for coordinate in self.ycoordinaat_lijst:
            coordinate = int(coordinate)
            for y in range(coordinate, (coordinate + bre)):
                if y == y_random:
                    self.place(id)
            for y in range(coordinate, (coordinate - bre)):
                if y == y_random:
                    self.place(id)

        self.build_house(id, x_random, y_random)

    def place(self, id):
        woning = self.woningen[id - 1]
        len = woning.lengte
        bre = woning.breedte
        VRIJSTAND = woning.minvrijstand

        # lengte = horizontaal
        # breedte = verticaal

        x_random = rd.randrange(GRID_LEN - int(len * 2))
        y_random = rd.randrange(GRID_BRE - int(bre * 2))

        self.check_place(id, x_random, y_random)

        print(self.xcoordinaat_lijst, self.ycoordinaat_lijst)



if __name__ == "__main__":
    amstelhaege = Amstelhaege()
    # for i in range(12):
    amstelhaege.place(1)
   # for i in range(5):
   #     amstelhaege.place(2)
   # for i in range(3):
   #     amstelhaege.place(3)

    plt.show()





# Wilco
