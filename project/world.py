from civilization import *


def participants():
    if input("Do you want to participate? (y/N) ") == "y":
        first = PlayerCivilization("player")
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
        step = civa.step()
        if civa.state in civa.rewards:
            rewards.append(civa.rewards[civa.state][step])
        print(civa.state)
        step = civb.step()
        if civb.state in civb.rewards:
            rewards.append(civb.rewards[civb.state][step])
        print(civb.state)
    print(rewards)


flag = True

while flag:
    civ1, civ2 = participants()
    simulate(civ1, civ2)
    flag = input("Do you want to make another go? (y/N) ") == "y"
