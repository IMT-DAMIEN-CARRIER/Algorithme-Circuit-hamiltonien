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
NB_NODE = 0

# Recursive function which calculate minimal circuit
# previousTown = current circuit
# availableTown = not actually visited Town
def travelTown(previousTown, availableTown):
    global MINIMUM_CHEMIN
    global MINIMUM_DISTANCE
    global NB_CHEMIN
    global NB_NODE

    NB_NODE += 1

    if len(availableTown) > 0:
        # For each not visited Town
        for town in availableTown:
            # If actual distance + MAX distance to go back to firt Town
            # 
            if MINIMUM_DISTANCE != -1 \
                    and len(previousTown) > 0 \
                    and getFullDistance(previousTown) + getMaxDistanceToStartFromCurrent(previousTown, availableTown) > MINIMUM_DISTANCE :
                return

            newPreviousTown = previousTown.copy()
            # Add a new Town to actual circuit
            newPreviousTown.append(town)
            newAvailableTown = availableTown.copy()
            # Remove this Town from not visited Towns
            newAvailableTown.remove(town)
            # Recursion
            travelTown(newPreviousTown, newAvailableTown)
    else:
        # If there is no more town to visit
        NB_CHEMIN += 1
        # Return to home
        previousTown.append(previousTown[0])
        # Calcul circuit distance
        distance = getFullDistance(previousTown)

        if MINIMUM_DISTANCE == -1 or MINIMUM_DISTANCE > distance:
            MINIMUM_DISTANCE = distance
            MINIMUM_CHEMIN = previousTown.copy()


# Calculate full distance 
def getFullDistance(towns):
    distance = 0
    previousTown = towns[0]

    for town in towns[1:]:
        distance += townsWithDistance[previousTown][town]
        previousTown = town

    return distance

# Calculate maximal Distance to go back to home
def getMaxDistanceToStartFromCurrent(towns, availableTowns):
    maxDistance = 0

    for town in availableTowns:
        distance = townsWithDistance[towns[-1]][town]
        distance += townsWithDistance[towns[0]][town]

        if maxDistance == 0 or maxDistance < distance:
            maxDistance = distance

    return maxDistance


def time_expired(n, stack):

    print('EXPIRED :', time.ctime())

    print('Nombre de chemins calculés : {}'.format(NB_CHEMIN))
    print('Nombre de nodes : {}'.format(NB_NODE))
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
availableTowns = list(townsWithDistance.keys())
previousTowns = list(availableTowns[0])
travelTown(previousTowns, availableTowns[1:])

print('Exiting :', time.ctime())
print('Nombre de chemins calculés : {}'.format(NB_CHEMIN))
print('Nombre de nodes : {}'.format(NB_NODE))
print('Distance minimale trouvée : {}'.format(MINIMUM_DISTANCE))
print('Chemin minimal : {}'.format(MINIMUM_CHEMIN))
