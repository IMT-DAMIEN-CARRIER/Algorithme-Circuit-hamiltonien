# Damien Carrier - Arthur Duca - Clément Savinaud

import string
import math


# Read tsp file to get Town coordonates informations
def getTowns(fileName):  
    dict = {}
    filepath = 'fichiers_test/' + fileName
    # open file
    with open(filepath) as test_file:
        i = 0

        for line in test_file:
            row = line.split()
            x = row[0]
            y = row[1]
            # insert coordinates to dict
            dict[str(i)] = {'x': float(x), 'y': float(y)}
            i += 1

    return dict

# Calculate distance between two Towns
def getDistance(town1, town2):
    carreTownX = town2['x'] - town1['x']
    carreTownY = town2['y'] - town1['y']

    return math.sqrt(math.pow(carreTownX, 2)+math.pow(carreTownY, 2))

# For each Town, calculate distance to each other Town
def setDistances(dictTown):
    dictTownDist = {}
    # For each town
    for lettre, coord in dictTown.items():
        # Create corresponding dict
        if lettre not in dictTownDist:
            dictTownDist[lettre] = {}
        # For each other town
        for lettreCible, coordCible in dictTown.items():
            if lettre != lettreCible and lettreCible not in dictTownDist[lettre]:
                # Calculate distance between current and target town
                distance = getDistance(coord, coordCible)
                # Set distance value for current Town
                dictTownDist[lettre][lettreCible] = distance
                # Set distance for target Town
                if lettreCible not in dictTownDist:
                    dictTownDist[lettreCible] = {}
                    dictTownDist[lettreCible][lettre] = distance

    return dictTownDist