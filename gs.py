#!/usr/bin/env python3

#gs.py
#Christen Bowies
#9-5-2014
#Implement Gale-Shapely Algorithm
#None
#formated tables of stable matching

import time

startTime = time.clock()

guys= dict()
girls = dict()
guys = {
    'dan': ['ann', 'kay', 'bell', 'jen', 'jill', 'bri', 'jess', 'sam', 'tori', 'pam'],
    'ray': ['ann', 'kay', 'jen', 'jill', 'jess', 'bell', 'tori', 'sam', 'pam', 'bri'],
    'joe': ['bri', 'pam', 'tori', 'sam', 'bell', 'jill', 'jess', 'kay', 'ann', 'jen'],
    'ace': ['sam', 'bell', 'pam', 'tori', 'ann', 'jen', 'kay', 'jill', 'jess', 'bri'],
    'abe': ['bell', 'pam', 'sam', 'jen', 'ann', 'kay', 'jess', 'bri', 'jill', 'tori'],
    'bob': ['tori', 'bri', 'jill', 'bell', 'pam', 'sam', 'jess', 'jen', 'ann', 'kay'],
    'ned': ['jill', 'jess', 'bell', 'bri', 'tori', 'kay', 'jen', 'sam', 'pam', 'ann'],
    'pat': ['pam', 'tori', 'jess', 'bell', 'sam', 'ann', 'jill', 'bri', 'jen', 'kay'],
    'avi': ['jill', 'jess', 'kay', 'tori', 'ann', 'bell', 'jen','pam', 'sam', 'bri'],
    'ted': ['jen', 'sam', 'bri', 'jill', 'pam', 'tori', 'bell', 'kay', 'jess', 'ann']}

girls = {
    'ann': ['dan', 'ray', 'joe', 'ace', 'abe', 'bob', 'ned', 'pat', 'avi', 'ted'],
    'bell': ['ray', 'ace', 'bob', 'abe', 'joe', 'pat', 'ted', 'avi', 'dan', 'ned'],
    'bri': ['ned', 'dan', 'ted', 'avi', 'abe', 'bob', 'joe', 'ace', 'ray', 'pat'],
    'jen': ['joe', 'abe', 'avi', 'ray', 'ted', 'dan', 'ace', 'bob', 'ned', 'ace'],
    'jess': ['ace', 'dan', 'joe', 'ray', 'ted', 'ned', 'avi', 'bob', 'pat', 'abe'],
    'jill': ['abe', 'ray', 'bob', 'ted', 'avi', 'ned', 'pat', 'joe', 'dan', 'ace'],
    'kay': ['ted', 'avi', 'ace', 'abe', 'bob', 'ray', 'joe', 'dan', 'pat', 'ned'],
    'pam': ['avi', 'bob', 'ray', 'ace', 'ned', 'ted', 'joe', 'pat', 'dan', 'abe'],
    'sam': ['bob', 'joe', 'abe', 'ace', 'dan', 'ned', 'ted', 'pat', 'avi', 'ray'],
    'tori': ['pat', 'ned', 'ted', 'bob', 'ray', 'avi', 'ace', 'joe', 'abe', 'dan']}

def matching():
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
            print(" %s marries %s" %(suitor, female))
        else:
            female_preferences = girls[female]
            if female_preferences.index(fiance) > female_preferences.index(suitor):
                engaged[female] = suitor
                print(" %s drops %s for %s" % (female, fiance, suitor))
                if suitor_preferences:
                    singlemen.append(fiance)
            else:
                if suitor_preferences:
                    singlemen.append(suitor)
    return engaged
    #returns list of engaged pairs

def main():
    print("Participants:")

    part = list(guys.keys())
    part2 = list(girls.keys())
    for i in range(len(part)):
        print (part[i], " ", end="")

    for i in range(len(part2)):
        print(part2[i], " ", end="")
    print()
    print()
    listing = list(guys.keys())
    listing2 = list(girls.keys())
    print("Preferences:")    
    for i in range(len(listing)):
        man = listing.pop(0)
        print(" %s : %s " % (man, guys[man]))
    for i in range(len(listing2)):
        woman = listing2.pop(0)
        print(" %s : %s " % (woman, girls[woman]))
    print()
    print("Marriages:")
    print()
    
    run = matching()
    
    print()
    
    print("Matches:")
    print()
    
    for i in sorted(run.items()):
        print(" %s and %s" % (i[0], i[1]))
        
    print()
    #calculate run time of function(matching) in milliseconds
    elapsedTime = time.clock()
    print("Time elapsed %f seconds" % (elapsedTime - startTime))
main()
    
            
        
        
