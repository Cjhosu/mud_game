from evennia import utils
from world.helpers import equipped_check, get_num_dice, DiceRoll
from world.rules.levels import XP
from world.combat.death import Death
import random

class CombatHandler():
    defense_score ={}
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
        attack_weapon = self.get_attack_weapon(caller)
        attack_attr =  self.get_attack_attribute()
        if not attack_attr:
            return
        init_attack_score = self.get_attack_score(attack_weapon,attack_attr)
        attack_score = round(random.uniform(1.0,1.5)* init_attack_score)
        if target:
            if not caller.search(target, location = caller.location):
                return
            else:
                target = self.caller.search(self.target)
                defense_score = self.get_defense_score(target)

                #What attribute do you use to attack?
                resolve = self.resolve_attack(defense_score, attack_score, attack_weapon, target)
                dealt_damage = resolve[0]
                if dealt_damage != None and dealt_damage > 0:
                    target.db.health -= dealt_damage
                damage_msg = resolve[1]
                caller.location.msg_contents(damage_msg)
                if target.db.health <= 0:
                    dead = Death(target)

        else:
            caller.msg("You test your might... You attack the air with " + str(attack_weapon) +" for an attack score of " + str(attack_score))

    def get_attack_weapon(self, caller):
        is_equipped = equipped_check(self.caller, "weapon")
        if is_equipped[0] == True:
            slots = caller.db.slots
            attack_weapon = slots["weapon"]
        else:
            attack_weapon = "your fists" 
        return attack_weapon

    def get_attack_attribute(self):
        caller = self.caller
        charclass = caller.db.charclass
        #find your favored attribute based on your class
        if not charclass:
            caller.msg("You should pick a class before you go picking fights! (Talk to Caroline at Shieldmaiden's)")
        else:
            attack_attr = self.charclass_attack_attr_dict[charclass]
            return attack_attr

    #Your weapon will do more for you if you know how to use it
    def weapon_multiplier(self,weapon, attack_attr):
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
        if weapon == "your fists":
            attack_score = caller.db.strength
        else:
            multiplier = self.weapon_multiplier(weapon, attack_attr)
            attack_score = attr_val + multiplier
        stance = self.caller.db.stance

        # If your stance is set to aggressive you gain a 10% attack advantage pre-all other buffs
        if stance == "aggressive":
            attack_score *= (1.1)
        return attack_score

    def get_defense_score(self, target):
        caller = self.caller
        is_equipped = equipped_check(target, "armor")
        if is_equipped[0] == True:
            slots = target.db.slots
            defense_bonus = slots["armor"].db.defense_bonus or 0
        else:
            defense_bonus = 0
        defense_score = target.db.defense + defense_bonus
        return defense_score

    def resolve_attack(self, defense_score, attack_score, attack_weapon, target):

        dealt_damage = attack_score - defense_score

        # If your stance is evasive or defensive you have a chance to avoid damage
        stance = target.db.stance
        if stance in ("evasive", "defensive"):
            if stance == "evasive":
                dex = target.db.dex
                stat = dex
            elif stance == "defensive":
                defense = target.db.defense
                stat = defense

            num_dice = get_num_dice(stat) or 1
            dice = DiceRoll(num_dice, pass_cond = [1])
            passed = dice.roll()[1]

            if passed == True and stance == "evasive":
                dealt_damage = None
                message = str(target) + " dodges and takes no damage!"
            elif passed == True and stance == "defensive":
                dealt_damage = None
                message = str(target) + " blocks and takes no damage!"
        if dealt_damage != None and dealt_damage > 0:
            xp = XP(self.caller, 30)
            message = str(self.caller) + " attacked "+ str(target) + " for " + str(dealt_damage)
            if not utils.inherits_from(self.caller, 'typeclasses.characters.NPC'):
                message += " with " + str(attack_weapon)

        elif dealt_damage != None and dealt_damage <= 0:
            message = str(target) + " shrugs off an attack from " + str(self.caller)
        return dealt_damage, message
