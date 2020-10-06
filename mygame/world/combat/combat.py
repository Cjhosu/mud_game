from commands.command import Command
from world.helpers import equipped_check
import random

class CombatHandler():
    target = {}
    caller = {}
    charclass_attack_attr_dict = {
        "Ranger" : "dex",
        "Warrior" : "strength",
        "Mage" : "magic",
        "Druid" : "magic",
        "Rogue" : "dex",
        "Paladin" : "strength"
        }

    weapon_attack_attr_dict = {
            "sword" : "strength",
            "battleaxe" : "strength",
            "dagger" : "dex",
            "bow" : "dex",
            "staff" : "magic"
            }
        #If you have an equipped weapon attack with it...

    def init_combat(self, caller, target):
        weapon_check = equipped_check(self.caller, "weapon")
        is_equipped = weapon_check
        if target:
            if not caller.search(target, location = caller.location):
                return
        else:
            caller.msg("You test your might...")
        if is_equipped == True:
            caller.msg(is_equipped)
            slots = caller.db.slots
            attack_weapon = slots["weapon"]
            #What attribute do you use to attack?
            attack_attr =  self.get_attack_attribute()
            init_attack_score = self.get_attack_score(attack_weapon,attack_attr)
            attack_score = round(random.uniform(1.0,1.5)* init_attack_score)

            #Otherwise use your fists
        else:
            attack_weapon = "your fists"
            attack_score = round(random.uniform(1.0,1.5)* caller.db.strength)

        #save most recently computed attack
        caller.ndb.attack_score = attack_score

        #handle messaging
        message = "%s +attack%s with %s for a combat score of %s!"
        caller.msg(message % ("You", "",attack_weapon, attack_score))
        caller.location.msg_contents(message % (caller.key, "s", attack_weapon, attack_score), exclude=caller)

    def get_attack_attribute(self):
        caller = self.caller
        charclass = caller.db.charclass
        #find your favored attribute based on your class
        attack_attr = self.charclass_attack_attr_dict[charclass]
        return attack_attr

    def weapon_multiplier(self,weapon, attack_attr):
        #Your weapon will do more for you if you know how to use it
        caller=self.caller
        multiplier = round(weapon.db.damage * (random.uniform(1.25,1.85)))
        if self.weapon_attack_attr_dict[weapon.db.weapon_type] == attack_attr:
            multiplier
        else:
            multiplier = weapon.db.damage
        return multiplier

    def get_attack_score(self, weapon, attack_attr):
        caller = self.caller
        attr_val = caller.attributes.get(attack_attr)
        #Knowing your attack attribute and the weapon equipped, find if it has a buff
        multiplier = self.weapon_multiplier(weapon, attack_attr)
        attack_score = attr_val + multiplier
        return attack_score
    pass

class CmdAttack(Command):
    """
    issues an attack

    Usage: +attack

    This will calculate a new combat score based on your Strength.
    Your combat score is visible to everyone in the same location
    """

    key = "+attack"
    help_category = "mush"

    def func(self):
        caller = self.caller
        cmbt = CombatHandler()
        "parse target"
        if self.args:
            target = self.args.strip()
            cmbt.target = target
        else:
            target = None
        cmbt.caller = caller
        cmbt.init_combat(caller, target)


class resolve_attack():
    pass
