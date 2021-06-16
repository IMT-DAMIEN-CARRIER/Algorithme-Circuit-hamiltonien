import time

from coordinates import *
from datetime import datetime

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

# dict = getTowns('tsp4.txt')
# townsWithDistance = setDistances(dict)
#
# date_debut = datetime.now()
# travelTown([], list(townsWithDistance.keys()))
# date_fin = datetime.now()
#
print('Nombre de chemins calculés : {}'.format(NB_CHEMIN))
print('Distance minimale trouvée : {}'.format(MINIMUM_DISTANCE))
print('Chemin minimal : {}'.format(MINIMUM_CHEMIN))
#
# print(date_fin - date_debut)
