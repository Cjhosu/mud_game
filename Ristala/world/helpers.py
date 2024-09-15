import random


class DiceRoll:
    def __init__(self, stat, **kwargs):
        self.roll_modifier = self.get_roll_modifier(stat)
        self.pass_dc = kwargs.get("pass_dc") or None

    def roll(self):
        passed = False
        pass_dc = self.pass_dc
        die_result = random.randint(1, 20)
        total_roll = die_result + self.roll_modifier
        if total_roll >= pass_dc:
            passed = True
        return (passed, die_result, total_roll)

    def get_roll_modifier(self, stat):
        modifier = -5
        base = 50
        while base < stat and modifier < 19:
            base += 10
            modifier += 1
        return modifier


def equipped_check(caller, item):
    slots = caller.db.slots
    caller = str(caller)
    equipped = False

    if slots:
        if slots[item]:
            equipped = True
            message = caller + "has a " + item + " equipped"
        else:
            message = caller + "has no " + item + " equipped"
    else:
        message = caller + " has no equipment slots"

    return equipped, message


def display_prompt(caller):

    if not caller.db.health:
        health = 255
    else:
        health = caller.db.health

    if not caller.db.max_health:
        max_health = 255
    else:
        max_health = caller.db.max_health

    if not caller.db.level:
        level = 1
    else:
        level = caller.db.level

    if not caller.db.xp:
        xp = 0
    else:
        xp = caller.db.xp

    if not caller.db.next_level_xp:
        next_level_xp = 0
    else:
        next_level_xp = caller.db.next_level_xp

    if not caller.db.gold:
        gold = 0
    else:
        gold = caller.db.gold

    if not caller.db.mana:
        mana = 0
    else:
        mana = caller.db.mana

    if not caller.db.max_mana:
        max_mana = 0
    else:
        max_mana = caller.db.max_mana

    if caller.db.charclass in ["Mage", "Druid"]:
        prompt = "HP:%i/%i Mana:%i/%i Level:%i  XP:%i/%i  Gold:%i" % (
                health, max_health, mana, max_mana, level, xp, next_level_xp, gold
                )
    else:
        prompt = "HP:%i/%i  Level:%i  XP:%i/%i  Gold:%i" % (health, max_health, level, xp, next_level_xp, gold)
    caller.msg(prompt=prompt)


def drop_gold_pieces():
    num_list = [1, 2, 3]
    number = random.choices(num_list, weights=(4, 2, 1), k=1)
    return number[0]
