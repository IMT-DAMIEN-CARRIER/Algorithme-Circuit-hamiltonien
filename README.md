# Algorithme - Circuit hamiltonien
#### Damien Carrier - Arthur Duca - Clément Savinaud

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
| tsp1.txt  | 9         | 10   | 2923,63  | 60   | 2923,63  | 600  | 2923,63  |
| tsp2.txt  | 10        | 10   | 4107,83  | 60   | 4107,83  | 600  | 4107,83  |
| tsp3.txt  | 6         | 10   | 2084,99  | 60   | 2084,99  | 600  | 2084,99  |
| tsp4.txt  | 16        | 10   | 8890.88  | 60   | 8054.51  | 600  | 7238.65  |
| tsp5.txt  | 12        | 10   | 5358,50  | 60   | 4608.42  | 600  | 4592.72  |
| tsp6.txt  | 9         | 10   | 3213.31  | 60   | 3213,31  | 600  | 3213.31  |
| tsp7.txt  | 6         | 10   | 3049.06  | 60   | 3049,06  | 600  | 3049,06  |
| tsp8.txt  | 11        | 10   | 4104.85  | 60   | 3892,46  | 600  | 3892.46  |
| tsp9.txt  | 8         | 10   | 3505.01  | 60   | 3505,01  | 600  | 3505,01  |
| tsp10.txt | 20        | 10   | 4671.42  | 60   | 4644,07  | 600  | 4631,37  |

## Algorithme :

* main.py
```python
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
                if lettreCible not in dictTownDist:
                    dictTownDist[lettreCible] = {}
                    dictTownDist[lettreCible][lettre] = distance
    return dictTownDist
```