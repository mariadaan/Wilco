# Milou van Casteren en Maria Daan en AAAAD
# minor programmeren
# Heuristieken
# Amstelhaege

from woning import Woning
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import sys

GRID_LEN = 321
GRID_BRE = 361

sys.setrecursionlimit(16000)


class Amstelhaege():
    def __init__(self):
        self.woningen = self.load_woningen("woningen.txt")
        self.make_grid = self.make_grid()
        self.count = 0
        self.total_value = 0
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
        plt.xlim(0, GRID_LEN)
        plt.ylim(0, GRID_BRE)


    def build_house(self, id, x_random, y_random):
        woning = self.woningen[id - 1]
        len = woning.lengte
        bre = woning.breedte
        vrij = woning.minvrijstand * 2

        self.xcoordinaat_lijst.append(x_random)
        self.ycoordinaat_lijst.append(y_random)



        x1 = np.arange(x_random, (int(bre * 2) + x_random))
        y1 = np.arange(y_random, (int(len * 2) + y_random))

        x2 = np.arange((x_random - vrij), ((int(bre * 2) + x_random) + vrij))
        y2 = np.arange((y_random - vrij), ((int(len * 2) + y_random) + vrij))

        x1_mesh, y1_mesh = np.meshgrid(x1,y1,)
        x2_mesh, y2_mesh = np.meshgrid(x2,y2)
        plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
        plt.scatter(x1_mesh, y1_mesh, marker="s", c="r")

        if id == 1:
            plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
            plt.scatter(x1_mesh, y1_mesh, marker="s", c="r")
        elif id == 2:
            plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
            plt.scatter(x1_mesh, y1_mesh, marker="s", c="g")
        elif id == 3:
            plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
            plt.scatter(x1_mesh, y1_mesh, marker="s", c="b")


        self.count += 1
        self.value(id, x_random, y_random)

        print(self.xcoordinaat_lijst)
        print(self.ycoordinaat_lijst)



    def check_place(self, id, x_random, y_random):
        woning = self.woningen[id - 1]
        len = int(woning.lengte) * 2
        bre = int(woning.breedte) * 2
        vrij = int(woning.minvrijstand) * 2

        if (x_random - vrij) < 0 or (y_random - vrij) < 0:
            self.place(id)
            return 0
        elif (x_random + bre + vrij) > GRID_LEN or (y_random + len + vrij) > GRID_BRE:
            self.place(id)
            return 0

        x_tester = 0
        y_tester = 0

        print(id)


        for coordinate in self.xcoordinaat_lijst:
            coordinate = int(coordinate)
            for x in range(coordinate, (coordinate + bre + vrij)):
                if x == x_random:
                    print(coordinate)
                    print(coordinate + bre + vrij)
                    x_tester += 1
            for x in range((coordinate - bre - vrij), coordinate):
                if x == x_random:
                    print(coordinate)
                    print(coordinate - bre - vrij)
                    x_tester += 1
        for coordinate in self.ycoordinaat_lijst:
            coordinate = int(coordinate)
            for y in range(coordinate, (coordinate + len + vrij)):
                if y == y_random:
                    print(coordinate)
                    print(coordinate + len + vrij)
                    y_tester += 1
            for y in range((coordinate - len - vrij), coordinate):
                if y == y_random:
                    print(coordinate)
                    print(coordinate - len - vrij)
                    y_tester += 1

        print("x_tester: ", x_tester)
        print("y_tester: ", y_tester)
        if x_tester > 0 and y_tester > 0:
            self.place(id)
            return 0

        self.build_house(id, x_random, y_random)

    def place(self, id):
        woning = self.woningen[id - 1]
        len = woning.lengte
        bre = woning.breedte
        vrij = woning.minvrijstand

        # lengte = horizontaal = x
        # breedte = verticaal = y

        x_random = rd.randrange(GRID_LEN - int(len * 2))
        y_random = rd.randrange(GRID_BRE - int(bre * 2))

        print()
        print("x_random: ", x_random)
        print("y_random: ", y_random)

        self.check_place(id, x_random, y_random)
        if id == 1:
            number = 4
        elif id == 2:
            number = 5
        elif id == 3:
            number = 3

        if self.count < number:
            self.place(id)

    def value(self, id, x, y):
        woning = self.woningen[id - 1]
        price = woning.prijs

        self.total_value += price

        return self.total_value




if __name__ == "__main__":
    amstelhaege = Amstelhaege()

    amstelhaege.place(1)
    amstelhaege.count = 0
    amstelhaege.place(2)
    amstelhaege.count = 0
    amstelhaege.place(3)



    print("total value: ", amstelhaege.total_value)

    plt.show()





# Wilco
