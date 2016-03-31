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

    for y in range(0, numberofsims):
        civastats = allstats[y][0]
        civbstats = allstats[y][1]
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
        elif (civastats[3] == 1) and (civbstats[3] == 1):
            totalB += 2
            if civastats[4] == 'survives' and civbstats[4] == 'dies':
                BbeatsB += 1
                totalBdied += 1
            elif civastats[4] == 'dies' and civbstats[4] == 'survives':
                BbeatsB += 1
                totalBdied += 1
            elif civastats[4] == 'cooperates' and civbstats[4] == 'cooperates':
                BcooperatesB += 1
            elif civastats[4] == 'survives' and civbstats[4] == 'survives':
                BhidesfromB += 1
            else:
                print("-> " + str(civastats) + " AND " + str(civbstats))

    print("Total benevolent civilizations: " + str(totalB) + " (" + str(totalBdied) + " died)")
    print("Total malevolent civilizations: " + str(totalM) + " (" + str(totalMdied) + " died)")
    print("benevolent beats malevolent: " + str(BbeatsM))
    print("benevolent beats benevolent: " + str(BbeatsB))
    print("malevolent beats benevolent: " + str(MbeatsB))
    print("malevolent beats malevolent: " + str(MbeatsM))
    print("benevolent cooperates with benevolent: " + str(BcooperatesB))
    print("malevolent cooperates with benevolent: " + str(BcooperatesM))
    print("malevolent cooperates with malevolent: " + str(McooperatesM))
    print("benevolent hides from malevolent: " + str(BhidesfromM))
    print("benevolent hides from benevolent: " + str(BhidesfromB))
    print("malevolent hides from malevolent: " + str(MhidesfromM))


def simulate(civa, civb):
    print("-------------------------------------------------------------------")
    print("Modelling encounter for " + civa.name + " and " + civb.name)
    civa.encounter(civb)
    civb.encounter(civa)
    rewards = []
    turncounter = 0
    while len(rewards) == 0:
        stepa = civa.step()
        print("[" + str(turncounter) + "] Current state of " + civa.name + " is: " + narrativize[civa.state])
        stepb = civb.step()
        print("[" + str(turncounter) + "] Current state of " + civb.name + " is: " + narrativize[civb.state])
        if civa.state in civa.rewards:
            rewards.append(civa.rewards[civa.state][stepa])
            print(civa.name + " civilization finishes. It " + str(civa.rewards[civa.state][stepa]))
        if civb.state in civb.rewards:
            rewards.append(civb.rewards[civb.state][stepb])
            print(civb.name + " civilization finishes. It " + str(civb.rewards[civb.state][stepb]))
        turncounter += 1

    stats = []
    civastats = []
    civastats.append(civa.tech)
    civastats.append(civa.depth)
    civastats.append(civa.detectability)
    civastats.append(civa.attitude)

    civbstats = []
    civbstats.append(civb.tech)
    civbstats.append(civb.depth)
    civbstats.append(civb.detectability)
    civbstats.append(civb.attitude)

    if (civa.state == 'hide') or (civa.state == 'defended') or (civa.state == 'destroy') or (civa.state == 'preemptive') or (civa.state == 'discover') or (civa.state == 'newly born'):
        civastats.append('survives')
    elif (civa.state == 'contact'):
        civastats.append('cooperates')
    else:
        civastats.append('dies')

    if (civb.state == 'hide') or (civb.state == 'defended') or (civb.state == 'destroy') or (civb.state == 'preemptive') or (civb.state == 'discover') or (civb.state == 'newly born'):
        civbstats.append('survives')
    elif (civb.state == 'contact'):
        civbstats.append('cooperates')
    else:
        civbstats.append('dies')

    stats.append(civastats)
    stats.append(civbstats)
    return stats

flag = True

while flag:
    if input("a) multiple unattended simulations to collect statistics.\nb) manual simulations\nYour choice (a/B) ") == "a":
            numberofsims = int(input("How many simulations would you like to run? "))
            statsrun(numberofsims)
    else:
        civ1, civ2 = participants()
        simulate(civ1, civ2)

    flag = input("Do you want to have another go? (y/N) ") == "y"
