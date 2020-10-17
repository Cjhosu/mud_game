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
            print(die_result)
            if pass_cond and die_result in pass_cond:
                passed = True
                return(results,passed)
            elif pass_cond and die_result not in pass_cond:
                passed = False
            else:
                passed = None
        return(results, passed)
