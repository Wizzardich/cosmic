from civilization import *



def participants():
    if input("Do you want to participate? (y/N) ") == "y":
        first = PlayerCivilization("player")
        choice = input("Do you wish to choose an opponent? (b/m/N) ")
        if choice == "b":
            return first, BenevolentCivilization("somename2b")
        elif choice == "m":
            return first, MalevolentCivilization("somename2m")
    elif random.random() > 0.5:
        first = BenevolentCivilization("somename1b")
    else:
        first = MalevolentCivilization("somename1m")

    if random.random() > 0.5:
        second = BenevolentCivilization("somename2b")
    else:
        second = MalevolentCivilization("somename2m")
    return first, second


def statsrun(numberofsims):
    for x in range(0, numberofsims):
        print("Running...")
        if random.random() > 0.5:
            civ1 = BenevolentCivilization("somename1b")
        else:
            civ1 = MalevolentCivilization("somename1m")
            if random.random() > 0.5:
                civ2 = BenevolentCivilization("somename2b")
            else:
                civ2 = MalevolentCivilization("somename2m")
        simulate(civ1, civ2)

def simulate(civa, civb):
    civa.encounter(civb)
    civb.encounter(civa)
    rewards = []
    while len(rewards) == 0:
        stepa = civa.step()
        print(civa.state)
        stepb = civb.step()
        print(civb.state)
        if civa.state in civa.rewards:
            rewards.append(civa.rewards[civa.state][stepa])
        if civb.state in civb.rewards:
            rewards.append(civb.rewards[civb.state][stepb])
    print(rewards)


flag = True

while flag:
    if input("a) multiple unattended simulations to collect statistics.\nb) manual simulations\nYour choice (a/B) ") == "a":
            numberofsims = int(input("How many simulations would you like to run? "))
            statsrun(numberofsims)
    else:
        civ1, civ2 = participants()
        simulate(civ1, civ2)

    flag = input("Do you want to have another go? (y/N) ") == "y"
