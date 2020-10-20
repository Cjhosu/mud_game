import random

class DiceRoll:
    def __init__(self, dice, **kwargs):
        self.dice = dice
        self.pass_cond = kwargs.get("pass_cond") or None
    def roll(self):
        results = []
        pass_cond = self.pass_cond
        for die in range(0,self.dice):
            die_result = random.randint(1,12)
            results.append(die_result)
            if pass_cond and die_result in pass_cond:
                passed = True
                return(results,passed)
            elif pass_cond and die_result not in pass_cond:
                passed = False
            else:
                passed = None
        return(results, passed)

def get_num_dice(stat):
    num_dice = 1
    base = 110
    while base < stat and num_dice < 10:
        base += 10
        num_dice +=1
    return num_dice


def equipped_check(caller, item):
    slots = caller.db.slots
    caller = str(caller)
    equipped = False

    if slots:
        if slots[item]:
            equipped = True
            message = caller + "has a "+ item + " equipped"
        else:
            message = caller + "has no "+ item + " equipped"
    else :
        message = caller + " has no equipment slots"

    return equipped, message
