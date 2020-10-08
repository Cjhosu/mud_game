from world.helpers import equipped_check
import random

class CombatHandler():
    target = {}
    defense_score ={}
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
        is_equipped = equipped_check(self.caller, "weapon")
        attack_weapon = self.get_attack_weapon(caller)
        attack_attr =  self.get_attack_attribute()
        init_attack_score = self.get_attack_score(attack_weapon,attack_attr)
        attack_score = round(random.uniform(1.0,1.5)* init_attack_score)
        if target:
            if not caller.search(target, location = caller.location):
                return
            else:
                target = self.caller.search(self.target)
                defense_score = self.get_defense_score(target)
                caller.msg(defense_score)

                #What attribute do you use to attack?
                resolve = self.resolve_attack(target, defense_score, attack_score, attack_weapon)
                dealt_damage = resolve[0]
                damage_msg = resolve[1]

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
        if weapon == "your fists":
            attack_score = caller.db.strength
        else:
            multiplier = self.weapon_multiplier(weapon, attack_attr)
            attack_score = attr_val + multiplier
        return attack_score

    def get_defense_score(self, target):
        defense_score = target.db.defense
        if not defense_score:
            defense_score = 0
        return defense_score

    def resolve_attack(self, target, defense_score, attack_score, attack_weapon):
        dealt_damage = attack_score - defense_score
        if dealt_damage > 0:
            message = "You've attacked "+ self.target + " for " + str(dealt_damage) + " with "+str(attack_weapon)
        else:
            message = self.target + " shrugs off your attack."
        return dealt_damage, message
