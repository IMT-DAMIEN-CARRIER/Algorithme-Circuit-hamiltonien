from coordinates import *
from datetime import datetime

date_debut = datetime.now()
global towns
MINIMUM_DISTANCE = -1
MINIMUM_CHEMIN = []

NB_CHEMIN = 0

def travelTown(previousTown, availableTown):
    global MINIMUM_CHEMIN
    global MINIMUM_DISTANCE
    global NB_CHEMIN
    if len(availableTown) > 0:
        for town in availableTown:
            newPreviousTown = previousTown.copy()
            newPreviousTown.append(town)
            newAvailableTown = availableTown.copy()
            newAvailableTown.remove(town)
            travelTown(newPreviousTown, newAvailableTown)
            
    else:
        NB_CHEMIN += 1
        distance = getFullDistance(previousTown)
        if MINIMUM_DISTANCE == -1 or MINIMUM_DISTANCE > distance:
            MINIMUM_DISTANCE = distance
            MINIMUM_CHEMIN = previousTown.copy()

def getFullDistance(towns):
    distance = 0
    previousTown = towns[0]
    for town in towns[1:]:
        distance += townsWithDistance[previousTown][town]
        previousTown = town
    return distance

dict = getTowns('tsp10.txt')
townsWithDistance = setDistances(dict)

travelTown([], list(townsWithDistance.keys()))

print('Nombre de chemins calculés : {}'.format(NB_CHEMIN))
print('Distance minimale trouvée : {}'.format(MINIMUM_DISTANCE))
print('Chemin minimal : {}'.format(MINIMUM_CHEMIN))

date_fin = datetime.now()

print(date_fin-date_debut)