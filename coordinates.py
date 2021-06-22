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
