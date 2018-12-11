# Milou van Casteren en Maria Daan en AAAAD
# minor programmeren
# Heuristieken
# Amstelhaege

from woning import Woning
from coordinate import Coordinate
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import statistics as stat
import math
import time

GRID_LEN = 321 #x
GRID_BRE = 361 #y


class Amstelhaege():
    def __init__(self):
        self.woningen = self.load_woningen("woningen.txt")
        # self.make_grid = self.make_grid()
        self.count = 0
        self.xcoordinaat_lijst = []
        self.ycoordinaat_lijst = []
        self.all_woningen = []
        self.total_value = 0
        self.width = GRID_LEN
        self.height = GRID_BRE
        self.meters = []

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
        new_woning = self.woningen[id - 1]
        new_len = int(new_woning.lengte * 2)
        new_bre = int(new_woning.breedte * 2)
        new_vrij = new_woning.minvrijstand * 2

        checker = 0
        x_random = 0
        y_random = 0


        while checker == 0:
            x_random = rd.randrange(new_vrij, GRID_LEN - new_len - new_vrij)
            y_random = rd.randrange(new_vrij, GRID_BRE - new_bre - new_vrij)

            loop = 0
            huh = 0

            # ff om in ieder geval 1 huis te plaatsen
            if self.count == 0:
                checker += 1
            else:
                for placed_woning in self.all_woningen:
                    loop += 1
                    placed_id = placed_woning.coordinate[0]
                    placed_x = placed_woning.coordinate[1]
                    placed_y = placed_woning.coordinate[2]
                    placed_len = self.woningen[placed_id - 1].lengte * 2
                    placed_bre = self.woningen[placed_id - 1].breedte * 2

                    max_vrij = 0

                    # max_vrij = grootste vrijstand
                    if self.woningen[placed_id - 1].minvrijstand > new_woning.minvrijstand:
                        max_vrij = (self.woningen[placed_id - 1].minvrijstand) * 2
                    else:
                        max_vrij = (new_woning.minvrijstand) * 2

                    x_checker = 0
                    y_checker = 0


                    x_lower = int(x_random - max_vrij - placed_len)
                    x_upper = int(x_random + new_len + max_vrij)

                    if placed_x in range(x_lower, x_upper):
                        x_checker += 1

                    y_lower = int(y_random - max_vrij - placed_bre)
                    y_upper = int(y_random + new_bre + max_vrij)

                    if placed_y in range(y_lower, y_upper):
                        y_checker += 1

                    if x_checker > 0 and y_checker > 0:
                        huh +=1
                        break

                if huh == 0:
                    checker += 1

        self.build_house(id, x_random, y_random, new_len, new_bre, new_vrij)

    def build_house(self, id, x_random, y_random, new_len, new_bre, new_vrij):
        self.all_woningen.append(Coordinate())
        self.all_woningen[-1].add(id, x_random, y_random)
        self.count += 1


    def plot_houses(self):
        # make grid
        x = np.arange(0, GRID_LEN)
        y = np.arange(0, GRID_BRE)
        x_mesh, y_mesh = np.meshgrid(x,y)
        plt.scatter(x_mesh, y_mesh, marker="s", c="lightgreen")
        plt.xlim(0, GRID_LEN)
        plt.ylim(0, GRID_BRE)

        for woning in self.all_woningen:
            id = woning.coordinate[0]
            x_random = woning.coordinate[1]
            y_random = woning.coordinate[2]
            new_len = self.woningen[id - 1].lengte * 2
            new_bre = self.woningen[id - 1].breedte * 2
            new_vrij = self.woningen[id - 1].minvrijstand * 2


            x1 = np.arange(x_random, new_len + x_random)
            y1 = np.arange(y_random, new_bre + y_random)


            x2 = np.arange((x_random - new_vrij), (new_len + x_random + new_vrij))
            y2 = np.arange((y_random - new_vrij), (new_bre + y_random + new_vrij))

            x1_mesh, y1_mesh = np.meshgrid(x1,y1)
            x2_mesh, y2_mesh = np.meshgrid(x2,y2)

            if id == 1:
                plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
                plt.scatter(x1_mesh, y1_mesh, marker="s", c="r")
            elif id == 2:
                plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
                plt.scatter(x1_mesh, y1_mesh, marker="s", c="g")
            elif id == 3:
                plt.scatter(x2_mesh, y2_mesh, marker="s", c="w")
                plt.scatter(x1_mesh, y1_mesh, marker="s", c="b")
            elif id == 4:
                plt.scatter(x2_mesh, y2_mesh, marker="s", c="y")
                plt.scatter(x1_mesh, y1_mesh, marker="s", c="b")

        # plt.show()




    def random_hillclimber(self):
        for i in range(100):
            value1 = self.value()
            random_house_index = rd.randrange(0, 19)
            random_house_id = self.all_woningen[random_house_index].coordinate[0]
            deleted = self.all_woningen.pop(random_house_index)
            self.check_and_place(random_house_id)
            value2 = self.value()

            if value2 <= value1:
                # print("niet geaccepteerd: ", self.usd(value2))
                self.all_woningen.pop(-1)
                self.all_woningen.append(deleted)
            # else:
                # print("wel geaccepteerd: ", self.usd(value2))


    def semirandom_hillclimber(self):
        for i in range(100):
            value1 = self.value()
            random_house_index = self.meters.index(min(self.meters))
            random_house_id = self.all_woningen[random_house_index].coordinate[0]
            deleted = self.all_woningen.pop(random_house_index)
            self.check_and_place(random_house_id)
            value2 = self.value()

            if value2 <= value1:
                # print("niet geaccepteerd: ", self.usd(value2))
                self.all_woningen.pop(-1)
                self.all_woningen.append(deleted)
            # else:
                # print(self.meters)
                # print("wel geaccepteerd: ", self.usd(value2))
                # self.plot_houses()
                # plt.pause(0.01)


    def value(self):

        # huis 1
        self.total_value = 0
        self.meters = []

        for house in self.all_woningen:
            # eigenschappen huis 1
            id = house.coordinate[0]
            vrij = self.woningen[id - 1].minvrijstand * 2
            len = self.woningen[id - 1].lengte * 2
            bre = self.woningen[id - 1].breedte * 2

            # linkeronderhoek huis 1
            x_left = int(house.coordinate[1])
            y_lower = int(house.coordinate[2])

            # rechterbovenhoek huis 1
            x_right = int(x_left + len)
            y_upper = int(y_lower + bre)

            # punten inclusief vrijstand
            x_min = int(x_left - vrij)
            x_max = int(x_left + len + vrij)
            y_min = int(y_lower - vrij)
            y_max = int(y_lower + bre + vrij)

            afstanden = []

            # afstand tot randen van grid
            # afstanden.append(x_min)
            # afstanden.append(y_min)
            # afstanden.append(GRID_LEN - x_max)
            # afstanden.append(GRID_BRE - y_max)

            # huis 2
            for housee in self.all_woningen:
                # eigenschappen huis 2
                id2 = housee.coordinate[0]
                vrij2 = self.woningen[id2 - 1].minvrijstand * 2
                len2 = self.woningen[id2 - 1].lengte * 2
                bre2 = self.woningen[id2 - 1].breedte * 2

                # linkeronderhoek en rechterbovenhoek huis 2
                x_left2 = int(housee.coordinate[1])
                x_right2 = int(housee.coordinate[1] + len2)
                y_lower2 = int(housee.coordinate[2])
                y_upper2 = int(housee.coordinate[2] + bre2)

                # loodrechte afstanden: huizen liggen boven elkaar
                if x_left2 in range(x_left, x_right) or x_right2 in range(x_left, x_right):
                    if x_left == x_left2 and y_lower == y_lower2:
                        # zelfde huis, niet met zichzelf vergelijken
                        pass
                    elif y_lower > y_upper2:
                        # huis 1 ligt boven huis 2
                        afstanden.append(y_min - y_upper2)
                    elif y_upper < y_lower2:
                        # huis 1 ligt onder huis 2
                        afstanden.append(y_lower2 - y_max)

                # loodrechte afstanden: huizen liggen naast elkaar
                if y_lower2 in range(y_lower, y_upper) or y_upper2 in range(y_lower, y_upper):
                    if x_left == x_left2 and y_lower == y_lower2:
                        # zelfde huis, niet met zichzelf vergelijken
                        pass
                    elif x_min > x_right2:
                        # huis 1 ligt rechts van huis 2
                        afstanden.append(x_min - x_right2)
                    elif x_right < x_left2:
                        # huis 1 ligt links van huis 2
                        afstanden.append(x_left2 - x_max)

                # diagonale afstanden: huis 2 rechts van huis 1
                if x_left2 > x_right and y_lower2 > y_upper:
                    # huis 2 ligt rechtsboven huis 1
                    A = x_left2 - x_right
                    B = y_lower2 - y_upper
                    C = math.sqrt(A * A + B * B)
                    afstanden.append(C - vrij)

                elif x_left2 > x_right and y_upper2 < y_lower:
                    # huis 2 ligt rechtsonder huis 1
                    A = x_left2 - x_right
                    B = y_lower - y_upper2
                    C = math.sqrt(A * A + B * B)
                    afstanden.append(C - vrij)

                # diagonale afstanden: huis 2 links van huis 1
                if x_right2 < x_left and y_lower2 > y_upper:
                    # huis 2 ligt linksboven huis 1
                    A = x_left - x_right2
                    B = y_lower2 - y_upper
                    C = math.sqrt(A * A + B * B)
                    afstanden.append(C - vrij)

                elif x_right2 < x_left and y_upper2 < y_lower:
                    # huis 2 ligt linksonder huis 1
                    A = x_left - x_right2
                    B = y_lower - y_upper2
                    C = math.sqrt(A * A + B * B)
                    afstanden.append(C - vrij)


            extrameters = int(min(afstanden) / 2)
            if extrameters < 0:
                print("huis 1: ")
                print(id)
                print(x_left)
                print(y_lower)
                print("huis 2: ")
                print(id2)
                print(x_left2)
                print(y_lower2)
            self.meters.append(extrameters)
            house_value = self.woningen[id - 1].prijs + (self.woningen[id - 1].prijs * extrameters * self.woningen[id - 1].waardestijging)
            self.total_value += house_value
        return self.total_value


    def usd(self, value):
        """Format value as USD."""
        return f"€{value:,.2f}"

if __name__ == "__main__":

    hillclimber = []
    random = []
    semirandom_hillclimber = []

    for i in range(50):
        print(i+1)
        amstelhaege = Amstelhaege()

        huizenvariant = 20

        eengezins = int(huizenvariant * 0.6)
        bungalow = int(huizenvariant * 0.25)
        villa = int(huizenvariant * 0.15)
        # water = 4

        for j in range(villa):
            amstelhaege.check_and_place(3)
        for j in range(bungalow):
            amstelhaege.check_and_place(2)
        for j in range(eengezins):
            amstelhaege.check_and_place(1)
        # for i in range(water):
        #     amstelhaege.check_and_place(4)

        amstelhaege.value()
        startvalue = amstelhaege.total_value
        print("randomwaarde: ", amstelhaege.usd(startvalue))

        # amstelhaege.water()

        amstelhaege.random_hillclimber()
        amstelhaege.value()
        finalvalue = amstelhaege.total_value
        print("hillclimberwaarde: ", amstelhaege.usd(finalvalue))

        amstelhaege.semirandom_hillclimber()
        amstelhaege.value()
        semivalue = amstelhaege.total_value
        print("semirandomwaarde: ", amstelhaege.usd(semivalue))

        # amstelhaege.plot_houses()

        # plt.show()

        random.append(startvalue)
        hillclimber.append(finalvalue)
        semirandom_hillclimber.append(semivalue)


    print("gemiddelde waarde random:                 ", amstelhaege.usd(stat.mean(random)))
    print("gemiddelde waarde hillclimber:            ", amstelhaege.usd(stat.mean(hillclimber)))
    print("gemiddelde waarde semirandom hillclimber: ", amstelhaege.usd(stat.mean(semirandom_hillclimber)))
    print()
    print("standaardafwijking random:                ", amstelhaege.usd(stat.stdev(random)))
    print("standaardafwijking hillclimber:           ", amstelhaege.usd(stat.stdev(hillclimber)))
    print("standaardafwijking semirandom hillclimber:", amstelhaege.usd(stat.stdev(semirandom_hillclimber)))

    plt.xlabel('Waarde van de kaart -->')
    plt.ylabel('Hoevaak komt waarde voor -->')


    bins = len(random)-2
    plot1 = plt.hist(random, bins=bins, stacked=True, label="Random", color="b")
    plot2 = plt.hist(hillclimber, bins=bins, stacked=True, label="Hillclimber", color="g")
    plot3 = plt.hist(semirandom_hillclimber, bins=bins, stacked=True, label="Semi-random hillclimber", color="r")

    plt.show()





# Wilco
