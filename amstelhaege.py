# Milou van Casteren, Maria Daan en Ad Ruigrok van der Werve
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

GRID_LEN = 320 #x
GRID_BRE = 360 #y


class Amstelhaege():
    """
    Dit is de Amstelhaege class. Hierin zijn functies te vinden die het mogelijk
    maken om een plattegrond te maken van de fictieve wijk Amstelhaege.
    """
    def __init__(self):
        self.woningen = self.load_woningen("woningen.txt")
        self.count = 0
        self.all_woningen = []
        self.total_value = 0
        self.meters = []
        self.best_map = []


    def load_woningen(self, filename):
        """
        Laad de woningen in vanuit de filename.
        Returnt een lijst van woning objecten.
        """
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


    def start_algoritme(self):
        print(f"\nWelkom in Amstelhaege! Ik ben Wilco.\n\n"
                "Instructies:\n"
                "Stap 1: Kies 20, 40 of 60 huizen\n"
                "Stap 2: Kies uit algoritmes greedy (g), random (r), semirandom (sr) of simulated annealing (sa)\n"
                "Stap 3: Kies het aantal stappen dat de gekozen hillclimber moet zetten.\n"
                "Stap 4: Kies hoe vaak je wil dat het hele programma wordt uitgevoerd\n"
                "Stap 5: Kies of je een histogram (h) van alle resultaten of een kaart (k) van de beste kaart wil zien"
                f"\n")

        huizenvariant = input("Huizenvariant: ")
        while huizenvariant != '20' and huizenvariant != '40' and huizenvariant != '60':
            print("Kies uit 20, 40 of 60.")
            huizenvariant = input("Huizenvariant: ")
        huizenvariant = float(huizenvariant)

        algoritme = input("Algoritme: ")
        while algoritme != 'g' and algoritme != 'r' and algoritme != 'sr' and algoritme != 'sa':
            print("Kies uit g, r, sr of sa")
            algoritme = input("Algoritme: ")

        stappen = input("Stappen: ")
        while not stappen.isdigit():
            print("Kies een positief getal")
            stappen = input("Stappen: ")
        stappen = int(stappen)

        keren = input("Aantal uitvoeringen: ")
        while not keren.isdigit():
            print("Kies een positief getal")
            input("Aantal uitvoeringen: ")
        keren = int(keren)

        plot = input("Kaart of histogram: ")
        while plot != 'h' and plot != 'k':
            print("Kies uit h en k")
            input("Kaart of histogram: ")


        # aantal huizen bepalen
        eengezins = int(huizenvariant * 0.6)
        bungalow = int(huizenvariant * 0.25)
        villa = int(huizenvariant * 0.15)

        self.random_kaart(huizenvariant, eengezins, bungalow, villa)

        self.best_map = self.all_woningen
        formervalue = self.total_value
        resultaten = []

        for i in range(keren):
            self.all_woningen = []
            if algoritme == 'g':
                self.greedy(huizenvariant, villa, bungalow, eengezins)
                self.random_hillclimber(stappen)
            elif algoritme == 'r':
                self.random_kaart(huizenvariant, eengezins, bungalow, villa)
                self.random_hillclimber(stappen)
            elif algoritme == 'sr':
                self.random_kaart(huizenvariant, eengezins, bungalow, villa)
                self.semirandom_hillclimber(stappen)
            elif algoritme == 'sa':
                self.random_kaart(huizenvariant, eengezins, bungalow, villa)
                self.simulated_annealing(stappen)
            else:
                print("invalid input")

            finalvalue = self.value(self.all_woningen)
            resultaten.append(finalvalue)

            if finalvalue > formervalue:
                formervalue = finalvalue
                self.best_map = self.all_woningen

        if keren > 10:
            self.statistieken(resultaten)

        print("waarde best map:        ", self.euro(self.value(self.best_map)))

        if plot == 'h':
            # histogram plotten
            self.plot_histogram(resultaten)
        elif plot == 'k':
            #kaart plotten
            self.plot_houses(self.best_map)


    def random_kaart(self, huizenvariant, eengezins, bungalow, villa):
        lowerbound = 0

        # # bepalen waarboven de startwaarde moet liggen
        # if huizenvariant == 20:
        #     lowerbound = 11500000
        # elif huizenvariant == 40:
        #     lowerbound = 18500000
        # elif huizenvariant == 60:
        #     lowerbound = 25200000

        x_random = rd.randrange(0, 241)
        y_random = rd.randrange(0, 66)

        startvalue = 0

        # while startvalue < lowerbound:
        self.all_woningen = []
        self.build_house(4, x_random, y_random)
        for j in range(villa):
            self.check_and_place(3)
        for j in range(bungalow):
            self.check_and_place(2)
        for j in range(eengezins):
            self.check_and_place(1)

        startvalue = self.value(self.all_woningen)


    def greedy(self, huizenvariant, villa, bungalow, eengezins):
        # villa's plaatsen in de hoeken
        self.build_house(3, 12, 327)
        self.build_house(3, 286, 327)
        self.build_house(3, 286, 12)

        if huizenvariant > 20:
            self.build_house(3, 12, 12)
            for j in range(villa - 4):
                self.check_and_place(3)

        # water plaatsen aan de rechterzijkant van de kaart
        self.build_house(4, 241, 33)

        # bungalows en eengezinswoningen random plaatsen
        for j in range(bungalow):
            self.check_and_place(2)
        for j in range(eengezins):
            self.check_and_place(1)


    def random_hillclimber(self, stappen):
        for i in range(stappen):
            print(i)
            value1 = self.value(self.all_woningen)
            random_house_index = rd.randrange(0, 19)
            random_house_id = self.all_woningen[random_house_index].coordinate[0]
            deleted = self.all_woningen.pop(random_house_index)
            self.check_and_place(random_house_id)
            value2 = self.value(self.all_woningen)

            if value2 <= value1:
                self.all_woningen.pop(-1)
                self.all_woningen.append(deleted)


    def semirandom_hillclimber(self, stappen):
        for i in range(stappen):
            value1 = self.value(self.all_woningen)
            random_house_index = self.meters.index(min(self.meters))
            random_house_id = self.all_woningen[random_house_index].coordinate[0]
            deleted = self.all_woningen.pop(random_house_index)
            self.check_and_place(random_house_id)
            value2 = self.value(self.all_woningen)

            if value2 <= value1:
                self.all_woningen.pop(-1)
                self.all_woningen.append(deleted)


    def check_and_place(self, id):
        new_woning = self.woningen[id - 1]
        print(new_woning.lengte)
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

        self.build_house(id, x_random, y_random)

    def build_house(self, id, x_random, y_random):
        self.all_woningen.append(Coordinate())
        self.all_woningen[-1].add(id, x_random, y_random)
        self.count += 1


    def plot_houses(self, map):
        # make grid
        x = np.arange(0, GRID_LEN)
        y = np.arange(0, GRID_BRE)
        x_mesh, y_mesh = np.meshgrid(x,y)
        plt.scatter(x_mesh, y_mesh, marker="s", c="lightgreen")
        plt.xlim(0, GRID_LEN)
        plt.ylim(0, GRID_BRE)

        for woning in map:
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

        plt.show()


    def value(self, map):

        # huis 1
        self.total_value = 0
        self.meters = []

        for house in map:
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
            for housee in map:
                # eigenschappen huis 2
                id2 = housee.coordinate[0]
                if not id2 == 4:
                    vrij2 = self.woningen[id2 - 1].minvrijstand * 2
                    len2 = self.woningen[id2 - 1].lengte * 2
                    bre2 = self.woningen[id2 - 1].breedte * 2

                    # linkeronderhoek en rechterbovenhoek huis 2
                    x_left2 = int(housee.coordinate[1])
                    x_right2 = int(housee.coordinate[1] + len2)
                    y_lower2 = int(housee.coordinate[2])
                    y_upper2 = int(housee.coordinate[2] + bre2)

                    # loodrechte afstanden: huizen liggen boven elkaar
                    if x_left2 in range(x_left, x_right + 1) or x_right2 in range(x_left, x_right + 1):
                        if x_left == x_left2 and y_lower == y_lower2:
                            # zelfde huis, niet met zichzelf vergelijken
                            pass
                        elif y_lower >= y_upper2:
                            # huis 1 ligt boven huis 2
                            afstanden.append(y_min - y_upper2)
                        elif y_upper <= y_lower2:
                            # huis 1 ligt onder huis 2
                            afstanden.append(y_lower2 - y_max)

                    # loodrechte afstanden: huizen liggen naast elkaar
                    if y_lower2 in range(y_lower, y_upper + 1) or y_upper2 in range(y_lower, y_upper + 1):
                        if x_left == x_left2 and y_lower == y_lower2:
                            # zelfde huis, niet met zichzelf vergelijken
                            pass
                        elif x_min >= x_right2:
                            # huis 1 ligt rechts van huis 2
                            afstanden.append(x_min - x_right2)
                        elif x_right <= x_left2:
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
            self.meters.append(extrameters)
            house_value = self.woningen[id - 1].prijs + (self.woningen[id - 1].prijs * extrameters * self.woningen[id - 1].waardestijging)
            self.total_value += house_value
        return self.total_value


    def plot_histogram(self, resultaten):
        plt.xlabel('Waarde van de kaart -->')
        plt.ylabel('Hoevaak komt waarde voor -->')

        bins = len(resultaten)-2
        plot1 = plt.hist(resultaten, bins=bins, stacked=True, label="Random")
        plt.show()


    def statistieken(self, resultaten):
        print("gemiddelde waarde: ", self.euro(stat.mean(resultaten)))
        print("standaardafwijking: ", self.euro(stat.stdev(resultaten)))
        print("laagst gevonden waarde: ", self.euro(min(resultaten)))
        print("hoogst gevonden waarde: ", self.euro(max(resultaten)))


    def euro(self, value):
        """Format value as EURO."""
        return f"€{value:,.2f}"


if __name__ == "__main__":
    amstelhaege = Amstelhaege()
    amstelhaege.start_algoritme()


# Wilco
