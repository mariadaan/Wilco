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


    def place(self, id):
        woning = self.woningen[id - 1]
        len = woning.lengte
        bre = woning.breedte
        VRIJSTAND = woning.minvrijstand

        # lengte = horizontaal
        # breedte = verticaal

        x_random = rd.randrange(GRID_LEN - int(len * 2))
        y_random = rd.randrange(GRID_BRE - int(bre * 2))

        print(x_random, y_random)

        x1 = np.arange(x_random, (int(bre * 2) + x_random))
        y1 = np.arange(y_random, (int(len * 2) + y_random))

        x2 = np.arange((x_random - VRIJSTAND), ((int(bre * 2) + x_random) + VRIJSTAND))
        y2 = np.arange((y_random - VRIJSTAND), ((int(len * 2) + y_random) + VRIJSTAND))

        x1_mesh, y1_mesh = np.meshgrid(x1,y1)
        x2_mesh, y2_mesh = np.meshgrid(x2,y2)
        plt.scatter(x2_mesh, y2_mesh)
        plt.scatter(x1_mesh, y1_mesh)




if __name__ == "__main__":
    amstelhaege = Amstelhaege()
    for i in range(12):
        amstelhaege.place(1)
    for i in range(5):
        amstelhaege.place(2)
    for i in range(3):
        amstelhaege.place(3)
    plt.show()





# Wilco
