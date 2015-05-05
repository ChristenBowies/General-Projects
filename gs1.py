#!/usr/bin/env python3

#gs1.py
#Christen Bowies
#9-6-2014
#simple code to test and run g-s algorithm with large random input
#size of male/females
#size: run time
#1000  .87000

import random, time, sys
startTime = time.clock()
   
def matching(n):
    guys = dict()
    girls = dict()
    listing = list(range(0,n))
    for i in range(n):
        random.shuffle(listing)
        guys[i] = listing
        girls[i] = listing
    
    singlemen = list(guys.keys())
    engaged = {}
    while singlemen:
        suitor = singlemen.pop(0)
        suitor_preferences = guys[suitor]
        female = suitor_preferences.pop(0)
        #Check for female in engaged dictionary
        fiance = engaged.get(female)
        if not fiance:
            #Engage pair by adding to dictionary key:value
            engaged[female] = suitor
            #print(" %s marries %s" %(suitor, female))
        else:
            female_preferences = girls[female]
            if female_preferences.index(fiance) > female_preferences.index(suitor):
                engaged[female] = suitor
                #print(" %s drops %s for %s" % (female, fiance, suitor))
                if suitor_preferences:
                    singlemen.append(fiance)
            else:
                if suitor_preferences:
                    singlemen.append(suitor)
    return engaged

def main():
    #will eventually implement check for shell input...
    n = int(sys.argv[1])
    engaged = matching(n)
    #Calculate run time of matching function
    elapsedTime = time.clock()
    print("%d    %f" % (n ,(elapsedTime - startTime)))
main()
