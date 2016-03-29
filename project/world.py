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
    "defended": "succesfully defended itself"
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


def simulate(civa, civb):
    print("Modelling encounter for " + civa.name + " and " + civb.name)
    civa.encounter(civb)
    civb.encounter(civa)
    rewards = []
    while len(rewards) == 0:
        stepa = civa.step()
        print("Current state of " + civa.name + " is: " + narrativize[civa.state])
        stepb = civb.step()
        print("Current state of " + civb.name + " is: " + narrativize[civb.state])
        if civa.state in civa.rewards:
            rewards.append(civa.rewards[civa.state][stepa])
            print(civa.name + " civilization finishes. It " + str(civa.rewards[civa.state][stepa]))
        if civb.state in civb.rewards:
            rewards.append(civb.rewards[civb.state][stepb])
            print(civb.name + " civilization finishes. It " + str(civb.rewards[civb.state][stepb]))


flag = True

while flag:
    civ1, civ2 = participants()
    simulate(civ1, civ2)
    flag = input("Do you want to make another go? (y/N) ") == "y"
