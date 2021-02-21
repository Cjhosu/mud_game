from evennia import Command
from evennia.utils import evmenu

class XP:
    def  __init__(self,target, xp_val):
        self.xp_val = xp_val
        self.target = target
        self.add()

    def add(self):
        target = self.target
        target.db.xp += self.xp_val
        self.check_level(target.db.xp ,target.db.next_level_xp)

    def check_level(self, xp, next_level_xp):
        target = self.target
        if target.db.xp >= target.db.next_level_xp:
            self.level_up()
            remainder = round(target.db.xp - target.db.next_level_xp)
            target.db.xp = remainder
            target.db.next_level_xp *= 1.5
            self.check_level(target.db.xp, target.db.next_level_xp)

    def level_up(self):
       self.target.db.level += 1
       self.target.location.msg_contents(str(self.target) +' has gained a level!')

class CmdLevelUp(Command):
    """
    Level up your attributes

    Usage:
        level
    """
    key = "level"

    def func(self):
        "Starts your level up menu"
        evmenu.EvMenu(self.caller, "world.rules.levels", startnode="spend_points")


def spend_points(caller):

    attr_points = caller.db.attr_points
    if attr_points > 0:
        text = "You have "+ str(attr_points) + " upgrade point(s) to spend. \n You can spend them on leveling your attributes.\n Pick one to upgrade!"
        options = ({"key": "_default", "goto": "parse_node"})
    else:
        text = "No points to spend"
        options = []
    return text, options

def parse_node(caller, raw_string):
    if (raw_string) in ["strength", "dex", "magic", "defense", "health", "intel", "luck"]:
        upgrade = caller.attributes.get(raw_string)
        caller.attributes.add(raw_string, upgrade + 1)
        caller.db.attr_points -= 1
        caller.msg("You have upgraded " + str(raw_string))
    else:
        caller.msg("You tried to upgrade "+ str(raw_string) +" instead choose strength, dex, magic, defense, health, intel, or luck")
    return spend_points(caller)
