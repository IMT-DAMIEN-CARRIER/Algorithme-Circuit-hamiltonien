from coordinates import *

global towns
global MINIMUMCHEMIN

dict = getTowns('tsp1.txt')
towns = setDistances(dict)


def plusCourtChemin():
    town = towns[]
