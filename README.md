# Amstelhaege

Ad Ruigrok van der Werve,
Milou van Casteren,
Maria Daan

## Case

De Amstelhaege case, een project van de Minor Programmeren van het vak Heuristieken. De case omvat het maken van een algoritme die een plattegrond genereert die een zo duur mogelijke wijk oplevert, dus een zo hoog mogelijke score. De oppervlakte van de plattegrond is 160x180 meter. Er is een grid gemaakt van de oppervlakte van de plattegrond in halve meters, dus van 320x360.

De case bestaat uit drie varianten, namelijk de 20-, 40- en 60-huizenvariant. De wijk bestaat uit 60% eensgezinswoningen, 25% bungalows en 15% villa's. Iedere soort woning heeft een specifieke oppervlakte, waarde, minimale vrijstand en waardestijging per extra meter vrijstand. Daarnaast is een vereiste dat 20% van het totale opppervlakte wordt bezet door water. Deze lichamen mogen vierhoeking of ovaal zijn en de hoogte-breedteverhoudingen moet tussen de 1 en 4 zijn.

De vrijstand van een woning is de kleinste afstand tot de dichstbijzijnde andere woning in de wijk. Elke extra meter vrijstand levert een waardestijging op, verschillend per woning. De vrijstand van woningen mogen overlappen en het oppervlaktewater is ook vrijstand. Het algoritme moet een indeling van de wijk opleveren waarbij woningen zo veel mogelijk vrijstand hebben. Op deze manier is de indeling van de woningen bepalend voor de waarde van de wijk.


## Upper bound

De upperbound wordt berekend aan de hand van de overgebleven oppervlakte na het plaatsen van alle huizen. De overgebleven vrijstand is in het meest optimistische geval allemaal extra vrijstand voor de woning met de hoogste waardestijging per extra meter vrijstand, in dit geval de villa. Bij de 20-huizenvariant zal de upperbound een waarde hebben van: €36.000.000


## Lower bound

De lower bound van de plattegrond is de minimale waarde die de plattegrond kan hebben. Deze bedraagt de waarde van alle woningen exclusief waardestijging voor extra meters vrijstand. Dit komt voor de 20-, 40-, en 60-huizenvariant uit op respectievelijk €7.245.000, €14.490.000 en €21.735.000.

## State space

De state space is een theoretische set van alle mogelijke indelingen van de wijk. In deze benadering kunnen ook huizen op elkaar worden gezet. De state space wordt berekend aan de hand van de mogelijke combinaties en de aantallen van de huizen. Voor de 20-huizenvariant is deze bij benadering (48000^12 * 45000^5 * 43000^3) = 3E79.


## Algo's

De algoritmes voor deze case zijn: randomized, hill climber en simulated annealing.

## Vereisten

Het programma is geschreven in python 3.7.0 in Atom(1.32.1). Het programma runt hierdoor alleen bij gebruik van python 3.7.0 of hoger.

### Acknowledgement


![(https://github.com/mariadaan/Wilco/blob/master/figuren/20%2C%20100%2C%2010000.png)]
