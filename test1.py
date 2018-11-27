# Milou van Casteren en Maria Daan en AAAAD
# minor programmeren
# Heuristieken
# Amstelhaege

from woning import Woning
from coordinate import Coordinate
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import sys

GRID_LEN = 321 #x
GRID_BRE = 361 #y

sys.setrecursionlimit(16000)


class Amstelhaege():
    def __init__(self):
        self.woningen = self.load_woningen("woningen.txt")
        self.make_grid = self.make_grid()
        self.count = 0
        self.total_value = 0
        self.xcoordinaat_lijst = []
        self.ycoordinaat_lijst = []
        self.all_woningen = []

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

    def check_and_place(self, id):
        woning = self.woningen[id - 1]
        len = int(woning.lengte * 2)
        bre = int(woning.breedte * 2)
        vrij = 0

        checker = 0
        x_random = 0
        y_random = 0

        while checker == 0:
            x_random = rd.randrange(vrij, GRID_LEN - len - vrij)
            y_random = rd.randrange(vrij, GRID_BRE - bre - vrij)

            print("x_random: ", x_random)
            print("y_random: ", y_random)

            # ff om in ieder geval 1 huis te plaatsen
            if self.count == 0:
                checker += 1
                vrij = woning.minvrijstand * 2
                break

            # if x_random and y_random are possible coordinates to place new house:
                # checker += 1

            for placed_woning in self.all_woningen:
                placed_id = placed_woning.coordinate[0]
                placed_x = placed_woning.coordinate[1]
                placed_y = placed_woning.coordinate[2]

                print("id:", placed_id)
                print("x:", placed_x)
                print("y:", placed_y)

                # vrij = grootste vrijstand
                if self.woningen[placed_id - 1].minvrijstand > woning.minvrijstand:
                    vrij = (self.woningen[placed_id - 1].minvrijstand) * 2
                else:
                    vrij = (woning.minvrijstand) * 2

                x_checker = 0
                y_checker = 0

                x_lower = int(placed_x - len - vrij)
                x_upper = int(placed_x + (self.woningen[placed_id - 1].lengte * 2) + vrij)

                if x_random in range(x_lower, x_upper):
                    x_checker += 1

                y_lower = int(placed_y - bre - vrij)
                y_upper = int(placed_y + (self.woningen[placed_id - 1].breedte * 2) + vrij)

                if y_random in range(y_lower, y_upper):
                    y_checker += 1

                if x_checker > 0 and y_checker > 0:
                    print("niet geplaatst")
                else:
                    checker += 1
                    break


        self.xcoordinaat_lijst.append(x_random)
        self.ycoordinaat_lijst.append(y_random)

        self.all_woningen.append(Coordinate())
        self.all_woningen[-1].add(id, x_random, y_random)


        # Build house
        x1 = np.arange(x_random, len + x_random)
        y1 = np.arange(y_random, bre + y_random)

        x2 = np.arange((x_random - vrij), (len + x_random + vrij))
        y2 = np.arange((y_random - vrij), (bre + y_random + vrij))

        x1_mesh, y1_mesh = np.meshgrid(x1,y1)
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





    # def build_house(self, id, x_random, y_random):
    #     woning = self.woningen[id - 1]
    #     len = woning.lengte
    #     bre = woning.breedte
    #     vrij = woning.minvrijstand * 2
    #
    #     self.xcoordinaat_lijst.append(x_random)
    #     self.ycoordinaat_lijst.append(y_random)
    #
    #     self.all_woningen.append(Coordinate())
    #     self.all_woningen[-1].add(id, x_random, y_random)
    #
    #     print("self.all_woningen: ", self.all_woningen)
    #
    #
    #     x1 = np.arange(x_random, (int(len * 2) + x_random))
    #     y1 = np.arange(y_random, (int(bre * 2) + y_random))
    #
    #     x2 = np.arange((x_random - vrij), ((int(len * 2) + x_random) + vrij))
    #     y2 = np.arange((y_random - vrij), ((int(bre * 2) + y_random) + vrij))
    #
    #     x1_mesh, y1_mesh = np.meshgrid(x1,y1,)
    #     x2_mesh, y2_mesh = np.meshgrid(x2,y2)
    #     plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
    #     plt.scatter(x1_mesh, y1_mesh, marker="s", c="r")
    #
    #     if id == 1:
    #         plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
    #         plt.scatter(x1_mesh, y1_mesh, marker="s", c="r")
    #     elif id == 2:
    #         plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
    #         plt.scatter(x1_mesh, y1_mesh, marker="s", c="g")
    #     elif id == 3:
    #         plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
    #         plt.scatter(x1_mesh, y1_mesh, marker="s", c="b")
    #
    #
    #     self.count += 1
    #     self.value(id, x_random, y_random)
    #
    #     print("alle x coordinaten: ", self.xcoordinaat_lijst)
    #     print("alle y coordinaten: ", self.ycoordinaat_lijst)
    #
    #
    #
    # def check_place(self, id, x_random, y_random):
    #     woning = self.woningen[id - 1]
    #     len = int(woning.lengte) * 2
    #     bre = int(woning.breedte) * 2
    #     vrij = int(woning.minvrijstand) * 2
    #
    #     if (x_random - vrij) < 0 or (y_random - vrij) < 0:
    #         self.place(id)
    #         return 0
    #     elif (x_random + len + vrij) > GRID_LEN or (y_random + bre + vrij) > GRID_BRE:
    #         self.place(id)
    #         return 0
    #
    #     x_tester = 0
    #     y_tester = 0
    #
    #     print("id: ", id)
    #
    #
    #     for coordinate in self.xcoordinaat_lijst:
    #         coordinate = int(coordinate)
    #         for x in range(coordinate, (coordinate + len + vrij)):
    #             if x == x_random:
    #                 x_tester += 1
    #         for x in range((coordinate - len - vrij), coordinate):
    #             if x == x_random:
    #                 x_tester += 1
    #     for coordinate in self.ycoordinaat_lijst:
    #         coordinate = int(coordinate)
    #         for y in range(coordinate, (coordinate + bre + vrij)):
    #             if y == y_random:
    #                 y_tester += 1
    #         for y in range((coordinate - bre - vrij), coordinate):
    #             if y == y_random:
    #                 y_tester += 1
    #
    #     print("x_tester: ", x_tester)
    #     print("y_tester: ", y_tester)
    #     if x_tester > 0 and y_tester > 0:
    #         self.place(id)
    #         return 0
    #
    #     self.build_house(id, x_random, y_random)
    #
    # def place(self, id):
    #     woning = self.woningen[id - 1]
    #     len = woning.lengte
    #     bre = woning.breedte
    #     vrij = woning.minvrijstand
    #
    #     # lengte = horizontaal = x
    #     # breedte = verticaal = y
    #
    #     x_random = rd.randrange(GRID_LEN - int(bre * 2))
    #     y_random = rd.randrange(GRID_BRE - int(len * 2))
    #
    #     print()
    #     print("x_random: ", x_random)
    #     print("y_random: ", y_random)
    #
    #     self.check_place(id, x_random, y_random)
    #     if id == 1:
    #         number = 20
    #     elif id == 2:
    #         number = 1
    #     elif id == 3:
    #         number = 1
    #
    #     if self.count < number:
    #         self.place(id)

    def value(self, id, x, y):
        woning = self.woningen[id - 1]
        price = woning.prijs

        self.total_value += price

        return self.total_value




if __name__ == "__main__":
    amstelhaege = Amstelhaege()

    # amstelhaege.place(1)
    # amstelhaege.count = 0
    # amstelhaege.place(2)
    # amstelhaege.count = 0
    # amstelhaege.place(3)

    for i in range(12):
        amstelhaege.check_and_place(1)
    for i in range(5):
        amstelhaege.check_and_place(2)
    for i in range(3):
        amstelhaege.check_and_place(3)

    for c in amstelhaege.all_woningen:
        print("id:", c.coordinate[0])
        print("x:", c.coordinate[1])
        print("y:", c.coordinate[2])
        print()

    plt.show()





# Wilco
