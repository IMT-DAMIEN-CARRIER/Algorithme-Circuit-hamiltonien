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
            if MINIMUM_DISTANCE != -1 \
                    and len(previousTown) > 0 \
                    and getFullDistance(previousTown) + getMaxDistanceToStartFromCurrent(previousTown, availableTown) > MINIMUM_DISTANCE :
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
print('Distance minimale trouvée : {}'.format(MINIMUM_DISTANCE))
print('Chemin minimal : {}'.format(MINIMUM_CHEMIN))
