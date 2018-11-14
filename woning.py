# Class woning

class Woning(object):

    def __init__(self, id, naam, lengte, breedte, prijs, minvrijstand, waardestijging):

        self.id = id
        self.naam = naam
        self.lengte = lengte
        self.breedte = breedte
        self.prijs = prijs
        self.minvrijstand = minvrijstand
        self.waardestijging = waardestijging
        # self.eindprijs =


    def __str__(self):
        return(str(self.id) + self.naam, self.lengte, self.breedte, self.prijs, self.minvrijstand, self.waardestijging)


    def eindprijs(self, extrameters):
        return self.prijs + (self.prijs * self.waardestijging) * extrameters
