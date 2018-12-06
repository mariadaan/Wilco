# Amstelhaege

Ad Ruigrok van der Werve,
Milou van Casteren,
Maria Daan

## Case

De Amstelhaege case, een project van de Minor Programmeren van het vak Heuristieken. De case omvat het maken van een algoritme die een plattegrond genereert die een zo duur mogelijke wijk oplevert, dus een zo hoog mogelijke score. De oppervlakte van de plattegrond is 160x180 meter. Er is een grid gemaakt van de oppervlakte van de plattegrond in halve meters, dus van 320x360.

De case bestaat uit drie varianten, namelijk de 20-, 40- en 60-huizenvariant. De wijk bestaat uit 60% eensgezinswoningen, 25% bungalows en 15% villa's. Iedere soort woning heeft een specifieke oppervlakte, waarde, minimale vrijstand en waardestijging per extra meter vrijstand. Daarnaast is een vereiste dat 20% van het totale opppervlakte wordt bezet door water. Deze lichamen mogen vierhoeking of ovaal zijn en de hoogte-breedteverhoudingen moet tussen de 1 en 4 zijn.

De vrijstand van een woning is de kleinste afstand tot de dichstbijzijnde andere woning in de wijk. Elke extra meter vrijstand levert een waardestijging op, verschillend per woning. De vrijstand van woningen mogen overlappen en het oppervlaktewater is ook vrijstand. Het algoritme moet een indeling van de wijk opleveren waarbij woningen zo veel mogelijk vrijstand hebben. Op deze manier is de indeling van de woningen bepalend voor de waarde van de wijk.


## Upper bound

De upperbound wordt berekend aan de hand van de overgebleven oppervlakte na het plaatsen van alle huizen. Stel er is 70.000 m2 over om te gebruiken als vrijstand. Daarnaast kan een huis maar maximaal met 4 huizen vrijstand delen, en minimaal met 2. De gemiddelde factor die uit deze omringing komt is circa 3,5. Het huis met relatief de meeste waardestijging per extra meter is de maison, en deze is €36.600 extra per meter extra.

De eerste extra meter vrijstand neemt 71 m2 in beslag, en dit levert dus per m2 de eerste meter extra circa €515 op. De upper bound kan dan worden berekend door deze eerste extra meter vrijstand te vermenigvuldigen met de overgebleven vrijstand, wat bij benadering op €36.000.000 uitkomt.

## Lower bound

De lower bound van de plattegrond is de minimale waarde die de plattegrond kan hebben. Deze wordt berekend aan de hand van de 20-huizenvariant zonder vrijstand meegerekend. Dit komt voor de 20-, 40-, en 60-huizenvariant uit op respectievelijk €7.245.000, €14.490.000 en €21.735.000.

## State space

The state space is a theoretical set of all possible combinations of the amount of house

De state space is een theoretische set van alle combinaties mogelijk om de plattegrond in te delen. In deze benadering kunnen ook huizen op elkaar worden gezet. De state space wordt berekend aan de hand van de mogelijke combinaties van de huizen. Voor de 20-huizenvariant is deze bijvoorbeeld bij benadering (48000^12 * 45000^5 * 43000^3) = 3^79.


## Algo's

De algoritmes voor deze case zijn: randomized, hill climber en simulated annealing.

## Vereisten

De vereisten van deze case zijn in ieder geval het gebruik van 3.7.0 of hoger. Daarnaast is deze case geschreven in de taal python in Atom(1.32.1).

### Acknowledgement
