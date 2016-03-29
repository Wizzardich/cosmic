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
    civ1, civ2 = participants()
    simulate(civ1, civ2)
    flag = input("Do you want to make another go? (y/N) ") == "y"
