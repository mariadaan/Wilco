# Milou van Casteren, Maria Daan en Ad Ruigrok van der Werve
# Heuristieken
# Amstelhaege

from house import House
from coordinate import Coordinate
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import statistics as stat
import math
import time

GRID_LEN = 320 #x
GRID_WID = 360 #y


class Amstelhaege():
    """
    This is the Amstelhaege class. It contains necessary attributes
    and methods to create a map that  the highest possible value.
    """

    def __init__(self):
        self.housetypes = self.load_houses("woningen.txt")
        self.count = 0
        self.all_houses = []
        self.total_value = 0
        self.meters = []
        self.best_map = []


    def load_houses(self, filename):
        """
        Loads houses from filename, returns a list of housetype objects
        """
        with open(filename, "r") as f:
            content = f.readlines()
            # Remove whitespace characters like `\n` at the end of each line.
            f = [x.strip() for x in content]
            houses = []
            itemnr = 0
            for item in f:
                # Add each type of house to a list
                if item == "~":
                    id = f[itemnr + 1]
                    name = f[itemnr + 2]
                    length = float(f[itemnr + 3])
                    width = float(f[itemnr + 4])
                    price = float(f[itemnr + 5])
                    min_space = float(f[itemnr + 6])
                    value_increase = float(f[itemnr + 7])
                    house = House(id, name, length, width, price, min_space, value_increase)
                    houses.append(house)
                    itemnr += 1
                else:
                    itemnr += 1
        return houses


    def start_algorithm(self):
        print(f"\nWelcome to Amstelhaege! My name is Wilco.\n\n"
                "Instructions:\n"
                "Step 1: Pick 20, 40 of 60 houses\n"
                "Step 2: Pick from the algorithms greedy (g), random (r) or semirandom (sr)\n"
                "Step 3: Pick the amount of steps the chosen hillclimber needs to take\n"
                "Step 4: Choose how many times you want the programme to be executed\n"
                "Step 5: Choose whether you want to see a histogram (h) of all results or a map (m) of the best result"
                f"\n")

        # Ensure valid input
        houses_quantity = input("Houses quantity: ")
        while houses_quantity != '20' and houses_quantity != '40' and houses_quantity != '60':
            print("Pick 20, 40 of 60.")
            houses_quantity = input("houses_quantity: ")
        houses_quantity = float(houses_quantity)

        algorithm = input("Algorithm: ")
        while algorithm != 'g' and algorithm != 'r' and algorithm != 'sr':
            print("Pick g, r or sr")
            algorithm = input("algorithm: ")

        steps = input("Steps: ")
        while not steps.isdigit():
            print("Choose a positive number")
            steps = input("steps: ")
        steps = int(steps)

        implementations = input("Executions: ")
        while not implementations.isdigit():
            print("Kies een positief getal")
            input("Aantal uitvoeringen: ")
        implementations = int(implementations)

        plot = input("Map or histogram: ")
        while plot != 'h' and plot != 'm':
            print("Kies uit h en m")
            input("map of histogram: ")

        # Determine amount of houses to build
        single_family = int(houses_quantity * 0.6)
        bungalow = int(houses_quantity * 0.25)
        villa = int(houses_quantity * 0.15)

        # Create random map
        self.random_map(houses_quantity, single_family, bungalow, villa)

        self.best_map = self.all_houses
        formervalue = self.total_value
        results = []

        # Run chosen algorithm as much times as inputted
        for i in range(implementations):
            self.all_houses = []
            if algorithm == 'g':
                self.greedy(houses_quantity, single_family, bungalow, villa)
                self.random_hillclimber(steps)
            elif algorithm == 'r':
                self.random_map(houses_quantity, single_family, bungalow, villa)
                self.random_hillclimber(steps)
            elif algorithm == 'sr':
                self.random_map(houses_quantity, single_family, bungalow, villa)
                self.semirandom_hillclimber(steps)
            elif algorithm == 'sa':
                self.random_map(houses_quantity, single_family, bungalow, villa)
                self.simulated_annealing(steps)
            else:
                print("invalid input")

            finalvalue = self.value(self.all_houses)
            results.append(finalvalue)

            # Save best map yet
            if finalvalue > formervalue:
                formervalue = finalvalue
                self.best_map = self.all_houses

        # Print statistics
        if implementations > 10:
            self.statistics(results)
        print("Value best map:        ", self.euro(self.value(self.best_map)))

        if plot == 'h':
            # Plot histogram
            self.plot_histogram(results)
        elif plot == 'm':
            # Plot map
            self.plot_houses(self.best_map)


    def random_map(self, houses_quantity, single_family, bungalow, villa):
        """
        Create a random map with a certain minimum value
        """

        # Build water at random x,y
        x_random = rd.randrange(0, 241)
        y_random = rd.randrange(0, 66)
        self.build_house(4, x_random, y_random)

        # Determine minimum value for starting point hillclimber
        lowerbound = 0
        if houses_quantity == 20:
            lowerbound = 12000000
        elif houses_quantity == 40:
            lowerbound = 15000000
        elif houses_quantity == 60:
            lowerbound = 20000000

        startvalue = 0
        while startvalue < lowerbound:
            # Build all houses at random places
            self.all_houses = []
            for j in range(villa):
                self.check_and_place(3)
            for j in range(bungalow):
                self.check_and_place(2)
            for j in range(single_family):
                self.check_and_place(1)
            startvalue = self.value(self.all_houses)
        print(startvalue)


    def greedy(self, houses_quantity, single_family, bungalow, villa):
        """
        Create a 'greedy' map with villas in the corners. The rest of the houses
        are placed random.
        """
        # Place villas in corners of the grid
        self.build_house(3, 12, 327)
        self.build_house(3, 286, 327)
        self.build_house(3, 286, 12)

        # Place additional villa in the remaining corner of the grid
        if houses_quantity > 20:
            self.build_house(3, 12, 12)
            for j in range(villa - 4):
                self.check_and_place(3)

        # Place water at rightside of the grid
        self.build_house(4, 241, 33)

        # Place bungalows and single family houses random on the grid
        for j in range(bungalow):
            self.check_and_place(2)
        for j in range(single_family):
            self.check_and_place(1)


    def random_hillclimber(self, steps):
        """
        Move a random house 'steps' amount of times
        """
        # Move random houses to a random new location
        for i in range(steps):
            print(i)
            value1 = self.value(self.all_houses)
            random_house_index = rd.randrange(0, 19)
            random_house_id = self.all_houses[random_house_index].coordinate[0]
            if not random_house_id == 4:
                deleted = self.all_houses.pop(random_house_index)
                self.check_and_place(random_house_id)
                value2 = self.value(self.all_houses)
                print(value2)
                # Only accept the move if the value of the map increases
                if value2 <= value1:
                    self.all_houses.pop(-1)
                    self.all_houses.append(deleted)


    def semirandom_hillclimber(self, steps):
        # Move house with the least space to a random new location
        for i in range(steps):
            value1 = self.value(self.all_houses)
            random_house_index = self.meters.index(min(self.meters))
            random_house_id = self.all_houses[random_house_index].coordinate[0]
            deleted = self.all_houses.pop(random_house_index)
            self.check_and_place(random_house_id)
            value2 = self.value(self.all_houses)
            # Only accept the move if the value of the map increases
            if value2 <= value1:
                self.all_houses.pop(-1)
                self.all_houses.append(deleted)


    def check_and_place(self, id):
        new_house = self.housetypes[id - 1]
        new_len = int(new_house.length * 2)
        new_wid = int(new_house.width * 2)
        new_space = new_house.min_space * 2

        checker = 0
        x_random = 0
        y_random = 0

        # Check if given position is valid
        while checker == 0:
            x_random = rd.randrange(new_space, GRID_LEN - new_len - new_space)
            y_random = rd.randrange(new_space, GRID_WID - new_wid - new_space)

            huh = 0

            # ff om in ieder geval 1 huis te plaatsen
            if self.count == 0:
                checker += 1
            else:
                for placed_house in self.all_houses:
                    placed_id = placed_house.coordinate[0]
                    placed_x = placed_house.coordinate[1]
                    placed_y = placed_house.coordinate[2]
                    placed_len = self.housetypes[placed_id - 1].length * 2
                    placed_wid = self.housetypes[placed_id - 1].width * 2

                    max_space = 0

                    # max_space = grootste spacestand
                    if self.housetypes[placed_id - 1].min_space > new_house.min_space:
                        max_space = (self.housetypes[placed_id - 1].min_space) * 2
                    else:
                        max_space = (new_house.min_space) * 2

                    x_checker = 0
                    y_checker = 0

                    x_lower = int(x_random - max_space - placed_len)
                    x_upper = int(x_random + new_len + max_space)

                    if placed_x in range(x_lower, x_upper):
                        x_checker += 1

                    y_lower = int(y_random - max_space - placed_wid)
                    y_upper = int(y_random + new_wid + max_space)

                    if placed_y in range(y_lower, y_upper):
                        y_checker += 1

                    if x_checker > 0 and y_checker > 0:
                        huh +=1

                if huh == 0:
                    checker += 1

        self.build_house(id, x_random, y_random)


    def build_house(self, id, x_random, y_random):
        self.all_houses.append(Coordinate())
        self.all_houses[-1].add(id, x_random, y_random)
        self.count += 1


    def plot_houses(self, map):
        # make grid
        x = np.arange(0, GRID_LEN)
        y = np.arange(0, GRID_WID)
        x_mesh, y_mesh = np.meshgrid(x,y)
        plt.scatter(x_mesh, y_mesh, marker="s", c="lightgreen")
        plt.xlim(0, GRID_LEN)
        plt.ylim(0, GRID_WID)

        for house in map:
            id = house.coordinate[0]
            x_random = house.coordinate[1]
            y_random = house.coordinate[2]
            new_len = self.housetypes[id - 1].length * 2
            new_wid = self.housetypes[id - 1].width * 2
            new_space = self.housetypes[id - 1].min_space * 2


            x1 = np.arange(x_random, new_len + x_random)
            y1 = np.arange(y_random, new_wid + y_random)


            x2 = np.arange((x_random - new_space), (new_len + x_random + new_space))
            y2 = np.arange((y_random - new_space), (new_wid + y_random + new_space))

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

        for house1 in map:
            # eigenschappen huis 1
            id = house1.coordinate[0]
            space = self.housetypes[id - 1].min_space * 2
            len = self.housetypes[id - 1].length * 2
            wid = self.housetypes[id - 1].width * 2

            # linkeronderhoek huis 1
            x_left = int(house1.coordinate[1])
            y_lower = int(house1.coordinate[2])

            # rechterbovenhoek huis 1
            x_right = int(x_left + len)
            y_upper = int(y_lower + wid)

            # punten inclusief spacestand
            x_min = int(x_left - space)
            x_max = int(x_left + len + space)
            y_min = int(y_lower - space)
            y_max = int(y_lower + wid + space)

            distances = []

            # afstand tot randen van grid
            # distances.append(x_min)
            # distances.append(y_min)
            # distances.append(GRID_LEN - x_max)
            # distances.append(GRID_WID - y_max)

            # huis 2
            for house2 in map:
                # eigenschappen huis 2
                id2 = house2.coordinate[0]
                if not id2 == 4:
                    space2 = self.housetypes[id2 - 1].min_space * 2
                    len2 = self.housetypes[id2 - 1].length * 2
                    wid2 = self.housetypes[id2 - 1].width * 2

                    # linkeronderhoek en rechterbovenhoek huis 2
                    x_left2 = int(house2.coordinate[1])
                    x_right2 = int(house2.coordinate[1] + len2)
                    y_lower2 = int(house2.coordinate[2])
                    y_upper2 = int(house2.coordinate[2] + wid2)

                    # loodrechte distances: huizen liggen boven elkaar
                    if x_left2 in range(x_left, x_right + 1) or x_right2 in range(x_left, x_right + 1):
                        if x_left == x_left2 and y_lower == y_lower2:
                            # zelfde huis, niet met zichzelf vergelijken
                            pass
                        elif y_lower >= y_upper2:
                            # huis 1 ligt boven huis 2
                            distances.append(y_min - y_upper2)
                        elif y_upper <= y_lower2:
                            # huis 1 ligt onder huis 2
                            distances.append(y_lower2 - y_max)

                    # loodrechte distances: huizen liggen naast elkaar
                    if y_lower2 in range(y_lower, y_upper + 1) or y_upper2 in range(y_lower, y_upper + 1):
                        if x_left == x_left2 and y_lower == y_lower2:
                            # zelfde huis, niet met zichzelf vergelijken
                            pass
                        elif x_min >= x_right2:
                            # huis 1 ligt rechts van huis 2
                            distances.append(x_min - x_right2)
                        elif x_right <= x_left2:
                            # huis 1 ligt links van huis 2
                            distances.append(x_left2 - x_max)

                    # diagonale distances: huis 2 rechts van huis 1
                    if x_left2 > x_right and y_lower2 > y_upper:
                        # huis 2 ligt rechtsboven huis 1
                        A = x_left2 - x_right
                        B = y_lower2 - y_upper
                        C = math.sqrt(A * A + B * B)
                        distances.append(C - space)

                    elif x_left2 > x_right and y_upper2 < y_lower:
                        # huis 2 ligt rechtsonder huis 1
                        A = x_left2 - x_right
                        B = y_lower - y_upper2
                        C = math.sqrt(A * A + B * B)
                        distances.append(C - space)

                    # diagonale distances: huis 2 links van huis 1
                    if x_right2 < x_left and y_lower2 > y_upper:
                        # huis 2 ligt linksboven huis 1
                        A = x_left - x_right2
                        B = y_lower2 - y_upper
                        C = math.sqrt(A * A + B * B)
                        distances.append(C - space)

                    elif x_right2 < x_left and y_upper2 < y_lower:
                        # huis 2 ligt linksonder huis 1
                        A = x_left - x_right2
                        B = y_lower - y_upper2
                        C = math.sqrt(A * A + B * B)
                        distances.append(C - space)
            extra_meters = int(min(distances) / 2)
            self.meters.append(extra_meters)
            house_value = self.housetypes[id - 1].price + (self.housetypes[id - 1].price * extra_meters * self.housetypes[id - 1].value_increase)
            self.total_value += house_value
        return self.total_value


    def plot_histogram(self, results):
        plt.xlabel('Waarde van de map -->')
        plt.ylabel('Hoevaak komt waarde voor -->')

        bins = len(results)-2
        plot1 = plt.hist(results, bins=bins, stacked=True, label="Random")
        plt.show()


    def statistics(self, results):
        print("gemiddelde waarde: ", self.euro(stat.mean(results)))
        print("standaardafwijking: ", self.euro(stat.stdev(results)))
        print("laagst gevonden waarde: ", self.euro(min(results)))
        print("hoogst gevonden waarde: ", self.euro(max(results)))


    def euro(self, value):
        """Format value as EURO."""
        return f"€{value:,.2f}"


if __name__ == "__main__":
    amstelhaege = Amstelhaege()
    amstelhaege.start_algorithm()


# Wilco
