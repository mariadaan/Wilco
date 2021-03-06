# Amstelhaege

Door Ad Ruigrok van der Werve, Milou van Casteren en Maria Daan

## Case

De Amstelhaege case, een project van de Minor Programmeren van het vak Heuristieken. De case omvat het maken van een algoritme die een plattegrond genereert die een zo duur mogelijke wijk oplevert, dus een zo hoog mogelijke score. De oppervlakte van de plattegrond is 160x180 meter. Er is een grid gemaakt van de oppervlakte van de plattegrond in halve meters, dus van 320x360.

De case bestaat uit drie varianten, namelijk de 20-, 40- en 60-huizenvariant. De wijk bestaat uit 60% eensgezinswoningen, 25% bungalows en 15% villa's. Iedere soort woning heeft een specifieke oppervlakte, waarde, minimale vrijstand en waardestijging per extra meter vrijstand. Daarnaast is een vereiste dat 20% van het totale opppervlakte wordt bezet door water. Deze lichamen mogen vierhoeking of ovaal zijn en de hoogte-breedteverhoudingen moet tussen de 1 en 4 zijn.

De vrijstand van een woning is de kleinste afstand tot de dichstbijzijnde andere woning in de wijk. Elke extra meter vrijstand levert een waardestijging op, verschillend per woning. De vrijstand van woningen mogen overlappen en het oppervlaktewater is ook vrijstand. Het algoritme moet een indeling van de wijk opleveren waarbij woningen zo veel mogelijk vrijstand hebben. Op deze manier is de indeling van de woningen bepalend voor de waarde van de wijk.


## Upper bound

De upperbound wordt berekend aan de hand van de overgebleven oppervlakte na het plaatsen van alle huizen. De overgebleven vrijstand is in het meest optimistische geval allemaal extra vrijstand voor de woning met de hoogste waardestijging per extra meter vrijstand, in dit geval de villa. Bij de 20-, 40- en 60-huizenvariant zal de upperbound respectievelijk een waarde hebben van: €36.500.000, €37.000.000 en €37.400.000


## Lower bound

De lower bound van de plattegrond is de minimale waarde die de plattegrond kan hebben. Deze bedraagt de waarde van alle woningen exclusief waardestijging voor extra meters vrijstand. Dit komt voor de 20-, 40-, en 60-huizenvariant uit op respectievelijk €7.245.000, €14.490.000 en €21.735.000.

## State space

De state space is een theoretische set van alle mogelijke indelingen van de wijk. In deze benadering kunnen ook huizen op elkaar worden gezet. De state space wordt berekend aan de hand van de mogelijke combinaties en de aantallen van de huizen. Voor de 20-huizenvariant is deze bij benadering (48000^12 * 45000^5 * 43000^3) = 3E79. Voor de 40-huizenvariant zal dit bij benadering (48000^24 * 45000^10 * 43000^6) = 5E186 zijn. Voor de 60-huizenvariant zal dit bij benadering (48000^36 * 45000^15 * 43000^9) = 1E280 zijn.


## Algoritmes

Er worden drie algoritmes gebruikt om de kaart in te delen. De eerste is een random hillclimber. Hierbij wordt eerst een volledig random kaart gemaakt. Het water wordt hierbij als 1 plas geplaatst met vaste afmetingen, wel op een random plek. Vervolgens worden telkens random huizen verplaatst als dit een waardestijging oplevert. Het water wordt niet meer verplaatst.

Het tweede algoritme noemen we de semi-random hillclimber. Dit algoritme komt voor een groot deel overeen met de random hillclimber, alleen wordt er nu niet telkens een random woning gekozen, maar de woning met de minste vrijstand. Deze wonging wordt vervolgens wel naar een random plek verplaatst.

Het laatste algortme is greedy. Deze is eigenlijk semi-greedy en semi-random, er wordt namelijk nog steeds veel random geplaatst en ge-hillclimbed. De villa's worden echter wel greedy geplaatst: in de hoeken. Omdat we de randen van de kaart niet als einde van de vrijstand zien, zijn dit gunstige plaatsen om de villa's veel vrijstand en dus waarde te geven. Ook het water wordt op een vaste locatie geplaatst: aan de zijkant van de kaart. Na het random plaatsen van de rest van de huizen, wordt hierop de random hillclimber uitgevoerd. Deze combinatie heeft geleid tot de hoogste resultaten.

## Gebruik

Bij het runnen van amstelhaege.py wordt vanzelf duidelijk hoe er met het programma omgegaan moet worden. De gebruiker bepaalt welk algoritme er gebruikt gaat worden, welke huizenvariant, hoeveel stappen de hillclimber moet zetten en hoe vaak het hele programma zich moet herhalen. Om de resultaten te vergelijken kan er een histogram geprint worden, maar je kan ook kiezen voor het tonen van de beste kaart. De bestanden coordinate.py en house.py representeren beide een huis. Bij coordinate.py gaat dit om een uniek huis, met x en y coordinaten. Bij house.py gaat dit om een type huis met alle eigenschappen erbij. Ook het water wordt gezien als een House object. In housetypes.txt worden deze types gedefineerd om ingeladen te kunnen worden in de housetype objects. Ten slotte is er nog make_histogram.py, wat een verouderde versie is die gebruikt kon worden om de algoritmes met elkaar te vergelijken en alle resultaten in één histogram te tonen.

## Vereisten

Het programma is geschreven in python 3.7.0 in Atom(1.32.1). Het programma runt hierdoor alleen bij gebruik van Python 3.7.0 of hoger.

#### Histogram


![blah](https://github.com/mariadaan/Wilco/blob/master/figuren/20%2C%20200%2C%201000.png)

Op bovenstaand histogram is te zien hoe onze algoritmes presteren als we het programma 200 keer herhalen en de hillclimber 1000 stappen laten zetten. De waardes horen bij de 20-huizenvariant. Blauw hoort bij random, groen bij onze volledig random hillclimber en rood bij onze semi-random hillclimber. Bij de semi-random hillclimber verplaatsen we het huis met de minste vrijstand.

#### Bijbehorende statistische cijfers

Gemiddelde waarde random:                  			€10,010,029.50

Gemiddelde waarde hillclimber:             			€14,513,262.90

Gemiddelde waarde semirandom hillclimber:  	    €14,783,520.75


Standaardafwijking random:                			€541,923.01

Standaardafwijking hillclimber:            			€513,024.55

Standaardafwijking semirandom hillclimber: 		  €554,368.70

#### Wat maken we hieruit op?

De gemiddelde waarde ligt bij de semi-random hillclimber meer dan €200,000.00 hoger dan bij de volledig random hillclimber. De standaardafwijking is echter ook groter, wat aantoont dat de semi-random hillclimber minder voorspelbaar is. De standaardafwijking is bij de semi-random hillclimber zelfs groter dan bij de random kaartenmaker. Het verschil in gemiddelde waarde tussen de hillclimber en de semi-random hillclimber wordt steeds kleiner naarmate we de hillclimber meer stappen laten zetten. Om deze reden kiezen we ervoor om met de beter betrouwbare volledig random hillclimber door te gaan.  


#### Plattegrond

Zie hier een voorbeeld van hoe een redelijk goede 20-huizen kaart eruit ziet:

![blah](https://github.com/mariadaan/Wilco/blob/master/figuren/20.png)
