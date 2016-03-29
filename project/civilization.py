import random

CIV_MAX_TECH = 10
CIV_MAX_SUSPICION_DEPTH = 5
CIV_MALEVOLENT_ATTITUDE = 0
CIV_BENEVOLENT_ATTITUDE = 1
CIV_MALEVOLENT_TRIGGER_HAPPY = 0.9
CIV_BENEVOLENT_TALKATIVE = 0.9
CIV_SURPRISE_BONUS = 2
CIV_DETECTABILITY = 0.5


class Civilization:

    def __init__(self, name):
        self.tech = random.random() * CIV_MAX_TECH
        self.depth = random.randint(0, CIV_MAX_SUSPICION_DEPTH)
        self.detectability = CIV_DETECTABILITY
        self.id = name
        self.state = "newly born"
        self.other = None
        self.automata = {
            "newly born": {"discover": 1.0, "newly born": 0.0}
        }

    def encounter(self, other):
        self.other = other
        self.automata["newly born"] = {"discover": other.detectability, "newly born": 1.0 - other.detectability}

    def discover(self):
        self.state = "discover"
        return True

    def hide(self):
        self.state = "hide"
        self.detectability *= 2
        self.tech += CIV_SURPRISE_BONUS
        return True

    def reset(self):
        self.state = "newly born"
        return True

    def die(self):
        self.state = "destroyed"
        return True

    def defended(self):
        self.state = "defended"
        return True


class MalevolentCivilization(Civilization):

    def __init__(self, name):
        Civilization.__init__(self, name)
        self.attitude = CIV_MALEVOLENT_ATTITUDE
        self.automata = {
            "newly born": {"discover": 1.0, "newly born": 0.0},
            "discover": {"destroy": CIV_MALEVOLENT_TRIGGER_HAPPY, "hide": 1 - CIV_MALEVOLENT_TRIGGER_HAPPY},
            "destroy": {"destroy": 0.0},
            "hide": {"hide": 0.0},
            "destroyed": {"destroyed": 0.0},
            "defended": {"defended": 0.0}
        }
        self.actions = {
            "newly born": self.reset,
            "discover": self.discover,
            "destroy": self.destroy,
            "hide": self.hide,
            "defended": self.defended
        }
        self.rewards = {
            "destroy": {True: "prevailed", False: "failed"},
            "hide": {True: "survives", False: "failed"},
            "destroyed": {True: "dies", False: "dies"},
            "defended": {True: "survives", False: "failed"}
        }

    def step(self):
        choices = self.automata[self.state]
        total = 0
        decision = random.random()
        for k, v in choices.items():
            total = total + v
            if decision < total:
                state = k
                break
        else:
            return True
        return self.actions[state]()

    def destroy(self):
        self.state = "destroy"
        if self.tech > self.other.tech:
            return self.other.die()
        else:
            self.die()
            self.other.defended()
            return False

    def contacted(self):
        return self.destroy()


class BenevolentCivilization(Civilization):
    def __init__(self, name):
        Civilization.__init__(self, name)
        self.attitude = CIV_BENEVOLENT_ATTITUDE
        contact, suspicion, hide = parse(self.suspicion_chain())

        self.automata = {
            "newly born": {"discover": 1.0, "newly born": 0.0},
            "discover": {
                "preemptive": suspicion,
                "contact": contact,
                "hide": hide
            },
            "preemptive": {"preemptive": 0.0},
            "contact": {"contact": 0.0},
            "hide": {"hide": 0.0},
            "destroyed": {"destroyed": 0.0},
            "defended": {"defended": 0.0}
        }
        self.actions = {
            "newly born": self.reset,
            "discover": self.discover,
            "contact": self.cooperate,
            "preemptive": self.preemptive,
            "hide": self.hide,
            "defended": self.defended
        }
        self.rewards = {
            "preemptive": {True: "survives", False: "failed"},
            "hide": {True: "survives", False: "failed"},
            "contact": {True: "cooperates", False: "tries"},
            "defended": {True: "survives", False: "failed"}
        }

    def step(self):
        choices = self.automata[self.state]
        total = 0
        decision = random.random()
        for k, v in choices.items():
            total = total + v
            if decision < total:
                state = k
                break
        else:
            return True
        return self.actions[state]()

    def preemptive(self):
        self.state = "preemptive"
        if self.tech > (self.other.tech - CIV_SURPRISE_BONUS):
            return self.other.die()
        else:
            self.die()
            return False

    def suspicion_chain(self):
        att = ""
        for i in range(0, self.depth):
            if random.random() > 0.5:
                att += str(CIV_MALEVOLENT_ATTITUDE)
                return att
            else:
                att += str(CIV_BENEVOLENT_ATTITUDE)
        return att

    def cooperate(self):
        self.state = "contact"
        self.other.contacted()
        return True

    def contacted(self):
        self.state = "contact"
        return True


def parse(attitudes):
    index = attitudes.find(str(CIV_MALEVOLENT_ATTITUDE))
    if index == -1:
        return CIV_BENEVOLENT_TALKATIVE, 0, 1 - CIV_BENEVOLENT_TALKATIVE
    elif index == 0:
        return 0, 0.5, 0.5
    else:
        return (1 - 0.1 - 0.5 / (2 ** index)), 0.5 / (2 ** index), 0.1


class PlayerCivilization(Civilization):
    def __init__(self, name):
        Civilization.__init__(self, name)

        self.automata = {
            "newly born":   ["discover", "newly born"],
            "discover":     ["destroy", "contact", "hide"],
        }
        self.actions = {
            "newly born": self.reset,
            "discover": self.discover,
            "destroy": self.destroy,
            "contact": self.cooperate,
            "hide": self.hide,
            "defended": self.defended
        }
        self.rewards = {
            "destroy": {True: "prevails", False: "failed"},
            "hide": {True: "survives", False: "failed"},
            "contact": {True: "cooperates", False: "tries"},
            "defended": {True: "survives", False: "failed"}
        }

    def encounter(self, other):
        self.other = other

    def step(self):
        choices = self.automata[self.state]
        print("Oh wise ruler! What should we do?")
        i = 0
        for choice in choices:
            print("\t" + str(i) + ". " + str(choice) + "?")
            i += 1
        decision = eval(input("What will it be, wise one? "))
        if decision >= len(choices):
            print("Then we will wait!")
            return
        return self.actions[choices[decision]]()

    def destroy(self):
        self.state = "destroy"
        if self.tech > self.other.tech:
            print("Yes, oh wise one. We prevailed and began the process of assimilation")
            return self.other.die()
        else:
            print("*static on top of loud noises and crackling of gunfire*")
            self.die()
            self.other.defended()
            return False

    def cooperate(self):
        self.state = "contact"
        print("We will contact other civilization immediately. Keep your fingers crossed so they don't destroy us.")
        self.other.contacted()
        return True

    def contacted(self):
        print("We received a transmission! We have two options:\n\t0. destroy?\n\t1. cooperate?")
        decision = eval(input("How shall we proceed? "))
        if decision == 0:
            print("We shall strike at those pesky creatures, and use all of their resources!")
            return self.destroy()
        elif decision == 1:
            print("They seem to be genuinely benevolent. Let us try to cooperate")
            self.state = "contact"
        else:
            print("We cannot just seat still and do nothing! Commander, proceed with the Exterminatus!")
            return self.destroy()
        return True
