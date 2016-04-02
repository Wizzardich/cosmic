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
    total = "n"
    died = "died"

    unrelated = ["newly born", "discover"]

    benevolent = {
        total: 0,
        died: 0,
        0: {"preemptive": 0, "contact": 0, "defended": 0, "hide": 0, "destroyed": 0},
        1: {"preemptive": 0, "contact": 0, "defended": 0, "hide": 0, "destroyed": 0}
    }

    malevolent = {
        total: 0,
        died: 0,
        0: {"destroy": 0, "defended": 0, "hide": 0, "destroyed": 0},
        1: {"destroy": 0, "defended": 0, "hide": 0, "destroyed": 0}
    }

    attitude = {
        CIV_MALEVOLENT_ATTITUDE: malevolent,
        CIV_BENEVOLENT_ATTITUDE: benevolent
    }

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
        simulate(civ1, civ2)
        attitude[civ1.attitude][total] += 1
        attitude[civ2.attitude][total] += 1

        if not (civ1.state in unrelated):
            attitude[civ1.attitude][civ2.attitude][civ1.state] += 1
        if not (civ2.state in unrelated):
            attitude[civ2.attitude][civ1.attitude][civ2.state] += 1

        if civ1.state == civ2.state:
            attitude[civ2.attitude][civ1.attitude][civ2.state] -= 1

        if civ1.state == "destroyed":
            attitude[civ1.attitude][died] += 1

        if civ2.state == "destroyed":
            attitude[civ2.attitude][died] += 1

    stop = timeit.default_timer()

    print("")
    print("======================================================================")
    print("             " + str(numberofsims) + " simulations completed in " + str(round((stop - start),2)) +" seconds")
    print("======================================================================")
    print("Total benevolent civilizations: " + str(attitude[CIV_BENEVOLENT_ATTITUDE][total]) +
          " (" + str(attitude[CIV_BENEVOLENT_ATTITUDE][died]) + " died)")
    print("Total malevolent civilizations: " + str(attitude[CIV_MALEVOLENT_ATTITUDE][total]) +
          " (" + str(attitude[CIV_MALEVOLENT_ATTITUDE][died]) + " died)")

    print("Malevolent destroys benevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_MALEVOLENT_ATTITUDE]["destroyed"]))
    print("Malevolent destroys malevolent: " +
          str(attitude[CIV_MALEVOLENT_ATTITUDE][CIV_MALEVOLENT_ATTITUDE]["destroyed"]))
    print("Malevolent hides from malevolent: " +
          str(attitude[CIV_MALEVOLENT_ATTITUDE][CIV_MALEVOLENT_ATTITUDE]["hide"]))
    print("Malevolent hides from benevolent: " +
          str(attitude[CIV_MALEVOLENT_ATTITUDE][CIV_BENEVOLENT_ATTITUDE]["hide"]))

    print("Benevolent defends against malevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_MALEVOLENT_ATTITUDE]["defended"]))
    print("Benevolent successfully makes a preemptive strike against malevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_MALEVOLENT_ATTITUDE]["preemptive"]))
    print("Benevolent hides from malevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_MALEVOLENT_ATTITUDE]["hide"]))
    print("Benevolent destroys benevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_BENEVOLENT_ATTITUDE]["preemptive"]))
    print("Benevolent defends against a preemptive strike benevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_BENEVOLENT_ATTITUDE]["defended"]))
    print("Benevolent hides from benevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_BENEVOLENT_ATTITUDE]["hide"]))
    print("Benevolent cooperates with benevolent: " +
          str(attitude[CIV_BENEVOLENT_ATTITUDE][CIV_BENEVOLENT_ATTITUDE]["contact"]))
    #print("Malevolent cooperates with benevolent: " + str(BcooperatesM))
    #print("Malevolent cooperates with malevolent: " + str(McooperatesM))

    # print("Avg CoS depth resulting in death: " + str(round((cosDie / cosDieTotal), 2)))
    # print("Avg CoS depth resulting in survival: " + str(round((cosSurvive / cosSurviveTotal),2)))
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

flag = True

while flag:
    choice = input("a) multiple unattended simulations to collect statistics.\n" +
                   "b) manual simulations\nYour choice (a/B) ")

    if choice == "a":
            numberOfSims = int(input("How many simulations would you like to run? "))
            statsrun(numberOfSims)
    else:
        Civilization.output = True
        civ1, civ2 = participants()
        simulate(civ1, civ2, True)
        Civilization.output = False

    flag = input("Do you want to have another go? (y/N) ") == "y"
