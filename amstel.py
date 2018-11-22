"""
Problem Set 6
Name: Maria Daan
Student Number: 11243406
"""

from room import Room
from item import Item
from inventory import Inventory

class Amstelhaege():
    """
    This is the Adventure game class. It contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """
    def __init__(self):
        """
        .
        """
        self.woningen = self.load_woningen("woningen.txt")


        self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
        self.items = self.load_items(f"data/{game}Items.txt")
        self.inventory = self.load_inventory()
        self.current_room = self.rooms[0]
        self.idlist = []
        self.player = Inventory()

    def load_woningen(self, filename):
        """
        Load rooms from filename.
        Returns a collection of Room objects.
        """
        with open(filename, "r") as f:
            woningen = []
            for regel in f:
                regel = regel.strip()

                # Add id, name and description to each room object
                if regel == "~":
                    regel = f.readline()
                    id = regel
                    regel = f.readline()
                    regel = regel.strip()
                    naam = regel
                    regel = f.readline()
                    regel = regel.strip()
                    lengte = regel
                    regel = f.readline()
                    regel = regel.strip()
                    breedte = regel
                    regel = f.readline()
                    regel = regel.strip()
                    prijs = regel
                    regel = f.readline()
                    regel = regel.strip()
                    minvrijstand = regel
                    regel = f.readline()
                    regel = regel.strip()
                    waardestijging = float(regel)
                    woning = Woning(id, naam, lengte, breedte, prijs, minvrijstand, waardestijging)
                    woningen.append(woning)
                print(woningen)

                # Add the connected routes to the room
                elif line.isupper():
                    line = line.split()
                    direction = line[0]
                    room_number = line[1]

                    # Add multiple routes to a direction if needed
                    if not direction in roomss[-1].connection:
                        roomss[-1].connection[direction] = [room_number]
                    else:
                        roomss[-1].connection[direction].append(room_number)
            return roomss

    def load_items(self, filename):
        """
        Load items from filename.
        Returns a collection of Item objects.
        """
        with open(filename, "r") as f:
            itemss = []
            for line in f:
                line = line.strip()
                # Add name, description and initial location to each item object
                if line.upper():
                    name = line
                    line = f.readline()
                    line = line.strip()
                    description = line
                    line = f.readline()
                    line = line.strip()
                    initial_room_id = line
                    item = Item(name, description, initial_room_id)
                    itemss.append(item)
                    line = f.readline()
            return itemss

    def load_inventory(self):
        """
        Adds items to their initial location
        """
        for item in self.items:
            self.rooms[int(item.initial_room_id) - 1].inventory.add(item)

    def won(self):
        """
        Check if the game is won.
        Returns a boolean.
        """
        if self.current_room.name == "Victory":
            return True
        else:
            return False

    def check(self, length):
        """
        Check which room the player needs to go to when a condition is involved
        """
        check = 0

        # Determine which direction meets the item-condition
        for value in self.room_num:
            if "/" in value:
                self.condition = value.split("/")
                for item_name in self.player.itemlist:
                    if self.condition[1] == item_name.name:
                        self.current_room = self.rooms[int(self.condition[0]) - 1]
                        check += 1

        # If no new room has been entered yet, go to the last room option
        if check == 0:
            self.current_room = self.rooms[int(self.room_num[length - 1]) - 1]

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        # Store the values in the connection dictionary in a list
        self.room_num = self.current_room.connection[direction]

        # Check if there is a conditional movement and change the current room
        if len(self.room_num) == 1:
            self.current_room = self.rooms[int(self.room_num[0]) - 1]
        else:
            adventure.check(len(self.room_num))

    def take(self, item_name):
        """
        Takes an item from the room
        """
        # Delete item from the current room's inventory
        item = self.current_room.inventory.remove(item_name)

        # Add item to player's inventory
        if item is not None:
            self.player.add(item)
            print(f"{item_name} taken.")
        else:
            print("No such item.")

    def drop(self, item_name):
        """
        Drops an item in to the room
        """
        # Delete item from the player's inventory
        item = self.player.remove(item_name)

        # Add item to the current room's inventory
        if item is not None:
            self.current_room.inventory.add(item)
            print(f"{item_name} dropped.")
        else:
            print("No such item.")

    def make(self):
        """
        Maak plattegrond
        """
        print(f"Welcome, to the Adventure games.\n"
            "May the randomly generated numbers be ever in your favour.\n"
            f"\n{adventure.current_room.description}")

        # Prompt the user for commands until they've won the game.
        while not self.won():
            # This method for FORCED only works on Small and Tiny,
            # it works until the end of CrowtherRooms, when FORCED is not the
            # only possible direction for a room. I am working on fixing this,
            # and I think I'm very close, but I won't be able to fix it in time.
            # I can send that version it by e-mail though, if you want!

            # For now, this handles the FORCED movements
            if len(adventure.current_room.connection) == 1:
                adventure.move("FORCED")
                if adventure.current_room.id in self.idlist:
                    print(adventure.current_room.name)
                else:
                    print(adventure.current_room.description)
                if len(adventure.current_room.inventory.itemlist) > 0:
                    for item in adventure.current_room.inventory.itemlist:
                        print(f"{item.name}: {item.description}")

            # Get a new direction from the user
            command = input("> ")
            command = command.upper()
            movements = [
                "NORTH", "SOUTH", "EAST", "WEST", "UP", "DOWN",
                "OUT", "IN", "XYZZY", "WAVE", "WATER", "JUMP"]
            abbreviations = {
                "Q": "QUIT", "L": "LOOK", "I": "INVENTORY", "N": "NORTH",
                "S": "SOUTH", "E": "EAST", "W": "WEST", "U": "UP", "D": "DOWN"}
            if command in abbreviations and len(command) == 1:
                command = abbreviations[command]

            # Check if the command is a valid movement
            if command in movements and self.current_room.isvalid(command):

                # Print appropriate room name/description after moving
                self.idlist.append(adventure.current_room.id)
                adventure.move(command)
                if adventure.current_room.id in self.idlist:
                    print(adventure.current_room.name)
                else:
                    print(adventure.current_room.description)

                # Print current room's inventory
                for item in adventure.current_room.inventory.itemlist:
                    print(f"{item.name}: {item.description}")

            # Handle any additional commands
            elif command == "HELP":
                print(f"You can move by typing directions such as EAST/WEST/IN/OUT\n"
                    "QUIT quits the game.\n"
                    "HELP prints instructions for the game.\n"
                    "INVENTORY lists the item in your inventory.\n"
                    "LOOK lists the complete description of the room and its contents.\n"
                    "TAKE <item> take item from the room.\n"
                    "DROP <item> drop item from your inventory.")
            elif command == "QUIT":
                print("Thanks for playing!")
                exit(0)
            elif command == "LOOK":
                print(adventure.current_room.description)
                if len(adventure.current_room.inventory.itemlist) > 0:
                    for item in adventure.current_room.inventory.itemlist:
                        print(f"{item.name}: {item.description}")
            elif len(command.split()) > 1:
                if command.split()[0] == "TAKE":
                    adventure.take(command.split()[1])
                elif command.split()[0] == "DROP":
                    adventure.drop(command.split()[1])
            elif command == "INVENTORY":
                if len(self.player.itemlist) > 0:
                    for item in self.player.itemlist:
                        print(f"{item.name}: {item.description}")
                else:
                    print("Your inventory is empty.")
            else:
                print("Invalid command.")
        exit(0)

if __name__ == "__main__":
    adventure.make()
