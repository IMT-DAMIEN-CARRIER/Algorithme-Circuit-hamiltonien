# Algorithme - Circuit hamiltonien



#### Equipe : Damien Carrier - Arthur Duca - Clément Savinaud

---



Cours de complexité algorithmique.
Mise en place d'un algorithme permettant de construire un circuit hamiltonien.

## Utilisation du script
```text
python main.py [nom du fichier] [temps d'éxécution max en secondes]
```

```shell
# Exemple : 
python main.py tsp1.txt 10
```

## Tableau des résultats

| Instance  | Nb villes | CPU  | Longueur | CPU  | Longueur | CPU  | Longueur |
| --------- | --------- | ---- | -------- | ---- | -------- | ---- | -------- |
| tsp1.txt  | 9         | 10   | 4156,62  | 60   | 4156,62  | 600  | 4156,62  |
| tsp2.txt  | 10        | 10   | 5197,59  | 60   | 5197,59  | 600  | 5197,59  |
| tsp3.txt  | 6         | 10   | 3195.98  | 60   | 3195.98  | 600  | 3195.98  |
| tsp4.txt  | 16        | 10   | 9111.16  | 60   | 8547.71  | 600  | 5715.23  |
| tsp5.txt  | 12        | 10   | 5528.11  | 60   | 5528.11  | 600  | 5528.11  |
| tsp6.txt  | 9         | 10   | 4363.38  | 60   | 4363.38  | 600  | 4363.38  |
| tsp7.txt  | 6         | 10   | 4468.31  | 60   | 4468.31  | 600  | 4468.31  |
| tsp8.txt  | 11        | 10   | 5053.57  | 60   | 5053.57  | 600  | 5053.57  |
| tsp9.txt  | 8         | 10   | 4597.87  | 60   | 4597.87  | 600  | 4597.87  |
| tsp10.txt | 20        | 10   | 5341.59  | 60   | 5314.23  | 600  | 4833.70  |

## Algorithme :

* main.py
```python
# Damien Carrier - Arthur Duca - Clément Savinaud

import time

from coordinates import *

# importing libraries
import signal
import resource
import sys

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
            if MINIMUM_DISTANCE != -1 and len(previousTown) > 0 and getFullDistance(previousTown) + getMaxPlusReturnTown(previousTown) > MINIMUM_DISTANCE:
                return
            newPreviousTown = previousTown.copy()
            newPreviousTown.append(town)
            newAvailableTown = availableTown.copy()
            newAvailableTown.remove(town)
            travelTown(newPreviousTown, newAvailableTown)
    else:
        NB_CHEMIN += 1
        previousTown.append(previousTown[0])
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

def getMaxPlusReturnTown(towns):
    distance = 0
    maxDistanceTown = townsWithDistance[towns[-1]]['MAX']
    distance += townsWithDistance[towns[-1]][maxDistanceTown]
    if maxDistanceTown != towns[0]:
        distance += townsWithDistance[maxDistanceTown][towns[0]]
    return distance

def time_expired(n, stack):

    print('EXPIRED :', time.ctime())

    print('Nombre de chemins calculés : {}'.format(NB_CHEMIN))
    print('Distance minimale trouvée : {}'.format(MINIMUM_DISTANCE))
    print('Chemin minimal : {}'.format(MINIMUM_CHEMIN))

    raise SystemExit(1)

def set_cpu_runtime(seconds):
    # Install the signal handler and set a resource limit
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    resource.setrlimit(resource.RLIMIT_CPU, (seconds, hard))
    soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
    print('Soft limit changed to :', soft)
    signal.signal(signal.SIGXCPU, time_expired)


fileName = sys.argv[1]
timestamp = int (sys.argv[2])

print('On lance le test pour le fichier : {}'.format(fileName))
print('On lance le test pour : {} secondes'.format(timestamp))

set_cpu_runtime(timestamp)

# Performing a CPU intensive task
print('Starting:', time.ctime())

dict = getTowns(fileName)
townsWithDistance = setDistances(dict)
travelTown([], list(townsWithDistance.keys()))

print('Exiting :', time.ctime())
print('Nombre de chemins calculés : {}'.format(NB_CHEMIN))
print('Distance minimale trouvée : {}'.format(MINIMUM_DISTANCE))
print('Chemin minimal : {}'.format(MINIMUM_CHEMIN))
```

* coordinates.py
```python
# Damien Carrier - Arthur Duca - Clément Savinaud

import string
import math

global lettres
lettres = list(string.ascii_uppercase)

def getTowns(fileName):
    dict = {}
    filepath = 'fichiers_test/' + fileName
    with open(filepath) as test_file:
        i = 0
        for line in test_file:
            row = line.split()
            x = row[0]
            y = row[1]
            dict[lettres[i]] = {'x':float(x),'y':float(y)}
            i += 1
    return dict

def getDistance(town1, town2):
    carreTownX = town2['x'] - town1['x']
    carreTownY = town2['y'] - town1['y']
    return math.sqrt(math.pow(carreTownX,2)+math.pow(carreTownY,2))

def setDistances(dictTown):
    dictTownDist = {}
    for lettre,coord in dictTown.items():
        if lettre not in dictTownDist:
            dictTownDist[lettre] = {}
        for lettreCible, coordCible in dictTown.items():
            if lettre != lettreCible and lettreCible not in dictTownDist[lettre]:
                distance = getDistance(coord,coordCible)
                dictTownDist[lettre][lettreCible] = distance
                if "MAX" not in dictTownDist[lettre]:
                    dictTownDist[lettre]["MAX"] = lettreCible
                elif dictTownDist[lettre][dictTownDist[lettre]["MAX"]] < distance:
                    dictTownDist[lettre]["MAX"] = lettreCible
                if lettreCible not in dictTownDist:
                    dictTownDist[lettreCible] = {}
                    dictTownDist[lettreCible][lettre] = distance
    return dictTownDist
```