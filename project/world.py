from civilization import *

benevolents = ["Quarian", "Asari", "United Federation", "Galactic Republic", "Culture", "KOMKOH", "Browncoats"]
malevolents = ["Idiran", "Klingon", "Galactic Empire", "The Reapers", "The Reavers", "Alliance"]
narrativize = {
    "newly born": "clueless and unsuspecting",
    "discover": "discovered another civilization",
    "destroy": "attempts to destroy another civilization",
    "preemptive": "attempts a preemptive strikes at another civilization " +
                  "due to belief of it being malevolent, or expecting a preemptive strike",
    "contact": "tries to make contact with another civilization",
    "hide": "hides",
    "destroyed": "was destroyed",
    "defended": "successfully defended itself"
}


def participants():
    subbenevolent = benevolents.copy()
    submalevolent = malevolents.copy()
    if input("Do you want to participate? (y/N) ") == "y":
        first = PlayerCivilization("player")
        choice = input("Do you wish to choose an opponent? (b/m/N) ")
        if choice == "b":
            return first, BenevolentCivilization(random.choice(benevolents))
        elif choice == "m":
            return first, MalevolentCivilization(random.choice(malevolents))
    elif random.random() > 0.5:
        first = BenevolentCivilization(random.choice(benevolents))
        subbenevolent.remove(first.name)
    else:
        first = MalevolentCivilization(random.choice(malevolents))
        submalevolent.remove(first.name)

    if random.random() > 0.5:
        second = BenevolentCivilization(random.choice(subbenevolent))
    else:
        second = MalevolentCivilization(random.choice(submalevolent))
    return first, second


def statsrun(numberofsims):
    allstats = []
    import timeit

    start = timeit.default_timer()

    for x in range(0, numberofsims):
        if random.random() > 0.5:
            civ1 = BenevolentCivilization(random.choice(benevolents))
        else:
            civ1 = MalevolentCivilization(random.choice(malevolents))
        if random.random() > 0.5:
            civ2 = BenevolentCivilization(random.choice(benevolents))
        else:
            civ2 = MalevolentCivilization(random.choice(malevolents))
        allstats.append(simulate(civ1, civ2))

    stop = timeit.default_timer()

    totalB = 0
    totalM = 0
    totalBdied = 0
    totalMdied = 0
    BbeatsM = 0
    MbeatsB = 0
    BbeatsB = 0
    MbeatsM = 0
    BhidesfromM = 0
    MhidesfromM = 0
    BhidesfromB = 0
    BcooperatesB = 0
    BcooperatesM = 0
    McooperatesM = 0
    cosDie = 0
    cosDieTotal = 0
    cosSurvive = 0
    cosSurviveTotal = 0

    for y in range(0, numberofsims):
        civastats = allstats[y][0]
        civbstats = allstats[y][1]
        # CivA benevolent and CivB malevolent
        if (civastats[3] == 1) and (civbstats[3] == 0):
            totalB += 1
            totalM += 1
            if civastats[4] == 'survives' and civbstats[4] == 'dies':
                totalMdied += 1
                BbeatsM += 1
            elif civastats[4] == 'dies' and civbstats[4] == 'survives':
                totalBdied += 1
                MbeatsB += 1
            elif civastats[4] == 'cooperates' and civbstats[4] == 'cooperates':
                BcooperatesM += 1
            elif civastats[4] == 'survives' and civbstats[4] == 'survives':
                BhidesfromM += 1
            else:
                print("-> " + str(civastats) + " AND " + str(civbstats))
        # CivA malevolent and CivB benevolent
        elif (civastats[3] == 0) and (civbstats[3] == 1):
            totalB += 1
            totalM += 1
            if civastats[4] == 'survives' and civbstats[4] == 'dies':
                MbeatsB += 1
                totalBdied += 1
            elif civastats[4] == 'dies' and civbstats[4] == 'survives':
                BbeatsM += 1
                totalMdied += 1
            elif civastats[4] == 'cooperates' and civbstats[4] == 'cooperates':
                BcooperatesM += 1
            elif civastats[4] == 'survives' and civbstats[4] == 'survives':
                BhidesfromM += 1
            else:
                print("-> " + str(civastats) + " AND " + str(civbstats))
        # CivA malevolent and CivB malevolent
        elif (civastats[3] == 0) and (civbstats[3] == 0):
            totalM += 2
            if civastats[4] == 'survives' and civbstats[4] == 'dies':
                MbeatsM += 1
                totalMdied += 1
            elif civastats[4] == 'dies' and civbstats[4] == 'survives':
                MbeatsM += 1
                totalMdied += 1
            elif civastats[4] == 'cooperates' and civbstats[4] == 'cooperates':
                McooperatesM += 1
            elif civastats[4] == 'survives' and civbstats[4] == 'survives':
                MhidesfromM += 1
            else:
                print("-> " + str(civastats) + " AND " + str(civbstats))
        # CivA benevolent and CivB benevolent
        elif (civastats[3] == 1) and (civbstats[3] == 1):
            totalB += 2
            if civastats[4] == 'survives' and civbstats[4] == 'dies':
                BbeatsB += 1
                totalBdied += 1
                cosSurvive += civastats[1]
                cosSurviveTotal += 1
                cosDie += civbstats[1]
                cosDieTotal += 1
            elif civastats[4] == 'dies' and civbstats[4] == 'survives':
                BbeatsB += 1
                totalBdied += 1
                cosSurvive += civbstats[1]
                cosSurviveTotal += 1
                cosDie += civastats[1]
                cosDieTotal += 1
            elif civastats[4] == 'cooperates' and civbstats[4] == 'cooperates':
                BcooperatesB += 1
                cosSurvive += civbstats[1]
                cosSurvive += civastats[1]
                cosSurviveTotal += 2
            elif civastats[4] == 'survives' and civbstats[4] == 'survives':
                BhidesfromB += 1
                cosSurvive += civbstats[1]
                cosSurvive += civastats[1]
                cosSurviveTotal += 2
            else:
                print("-> " + str(civastats) + " AND " + str(civbstats))

    print("")
    print("======================================================================")
    print("             " + str(numberofsims) + " simulations completed in " + str(round((stop - start),2)) +" seconds")
    print("======================================================================")
    print("Total benevolent civilizations: " + str(totalB) + " (" + str(totalBdied) + " died)")
    print("Total malevolent civilizations: " + str(totalM) + " (" + str(totalMdied) + " died)")

    print("Malevolent destroys benevolent: " + str(MbeatsB))
    print("Malevolent destroys malevolent: " + str(MbeatsM))
    print("Malevolent hides from malevolent: " + str(MhidesfromM))

    print("Benevolent destroys malevolent: " + str(BbeatsM))
    print("Benevolent hides from malevolent: " + str(BhidesfromM))
    print("Benevolent destroys benevolent: " + str(BbeatsB))
    print("Benevolent hides from benevolent: " + str(BhidesfromB))
    print("Benevolent cooperates with benevolent: " + str(BcooperatesB))
    #print("Malevolent cooperates with benevolent: " + str(BcooperatesM))
    #print("Malevolent cooperates with malevolent: " + str(McooperatesM))

    print("Avg CoS depth resulting in death: " + str(round((cosDie / cosDieTotal), 2)))
    print("Avg CoS depth resulting in survival: " + str(round((cosSurvive / cosSurviveTotal),2)))
    print("======================================================================")


def simulate(civa, civb, output = False):
    if output:
        print("----------------------------------------------------------------------")
        print("Modelling encounter for " + civa.name + " and " + civb.name)
    civa.encounter(civb)
    civb.encounter(civa)
    rewards = []
    turncounter = 0
    while len(rewards) == 0:
        stepa = civa.step()
        if output:
            print("[" + str(turncounter) + "] Current state of " + civa.name + " is: " + narrativize[civa.state])
        stepb = civb.step()
        if output:
            print("[" + str(turncounter) + "] Current state of " + civb.name + " is: " + narrativize[civb.state])
        if civa.state in civa.rewards:
            rewards.append(civa.rewards[civa.state][stepa])
            if output:
                print(civa.name + " civilization finishes. It " + str(civa.rewards[civa.state][stepa]))
        if civb.state in civb.rewards:
            rewards.append(civb.rewards[civb.state][stepb])
            if output:
                print(civb.name + " civilization finishes. It " + str(civb.rewards[civb.state][stepb]))
        turncounter += 1

    if not output:
        stats = []
        civa_stats = [civa.tech, civa.depth, civa.detectability, civa.attitude]
        civb_stats = [civb.tech, civb.depth, civb.detectability, civb.attitude]

        survive_states = ['hide', 'defended', 'destroy', 'preemptive', 'discover', 'newly born']

        if civa.state in survive_states:
            civa_stats.append('survives')
        elif civa.state == 'contact':
            civa_stats.append('cooperates')
        else:
            civa_stats.append('dies')

        if civb.state in survive_states:
            civb_stats.append('survives')
        elif civb.state == 'contact':
            civb_stats.append('cooperates')
        else:
            civb_stats.append('dies')

        stats.append(civa_stats)
        stats.append(civb_stats)
        return stats

flag = True

while flag:
    choice = input("a) multiple unattended simulations to collect statistics.\n" +
                   "b) manual simulations\nYour choice (a/B) ")

    if choice == "a":
            numberOfSims = int(input("How many simulations would you like to run? "))
            statsrun(numberOfSims)
    else:
        civ1, civ2 = participants()
        simulate(civ1, civ2, True)

    flag = input("Do you want to have another go? (y/N) ") == "y"
