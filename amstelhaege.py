# Milou van Casteren en Maria Daan en AAAAD
# minor programmeren
# Heuristieken
# Amstelhaege

from woning import Woning
import numpy as np
import matplotlib.pyplot as plt

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

        x = np.arange(0, 33)
        y = np.arange(0, 37)
        x1 = np.arange(8, 24)
        y1 = np.arange(9, 27)
        x_mesh, y_mesh = np.meshgrid(x,y)
        x1_mesh, y1_mesh = np.meshgrid(x1,y1)

        plt.scatter(x_mesh, y_mesh)
        plt.scatter(x1_mesh, y1_mesh)

        # plt.show()

    # def huizenvariant_20():
    #     eengezins_20 = 12
    #     bungalows_20 = 5
    #     villas_20 = 3
    #     combinatie_woningen = []


    def place(self, id):
        woning = self.woningen[id - 1]
        len = woning.lengte
        bre = woning.breedte

        x = np.arange(0, 33)
        y = np.arange(0, 37)
        x1 = np.arange(0, (len * 2))
        y1 = np.arange(0, (bre * 2))
        x_mesh, y_mesh = np.meshgrid(x,y)
        x1_mesh, y1_mesh = np.meshgrid(x1,y1)

        plt.scatter(x_mesh, y_mesh)
        plt.scatter(x1_mesh, y1_mesh)

        plt.show()



if __name__ == "__main__":
    amstelhaege = Amstelhaege()
    amstelhaege.place(4)




# Wilco
