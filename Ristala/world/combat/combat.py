from evennia import utils
from world.helpers import equipped_check, DiceRoll
from world.rules.levels import XP
import random


class CombatHandler():
    magic_attack_strings = [
            " bends the fabric of the universe to attack ",
            " summons a bolt of eldrich energy attacking ",
            " taps into an unseen well of magic sending a wave of destruction at "
            ]

    def init_combat(self, caller, target):
        weapon = self.get_attack_weapon(caller)
        weapon_type = self.weapon_type(weapon)
        attack_attr = self.get_attack_attribute()
        init_attack_score = self.get_attack_score(weapon, weapon_type, attack_attr)
        attack_score = round(random.uniform(1.0, 1.5) * init_attack_score)

        # Attacking without an intended target can give you a sense of how powerful your equipped weapon is
        if not target:
            self.message(None, attack_score, None, weapon, None, None)
            return

        # Your target must be in the same location as you
        if not caller.search(target, location=caller.location):
            return

        target = self.caller.search(self.target)
        defense_score = self.get_defense_score(target)
        resolve = self.resolve_attack(defense_score, attack_score, weapon, weapon_type, target)
        damage_msg = resolve[1]
        caller.location.msg_contents(damage_msg)

        # Update HP if needed
        dealt_damage = resolve[0]
        if dealt_damage is not None and dealt_damage > 0:
            target.db.health -= dealt_damage

        # Ya dead?
        if target.db.health <= 0:
            target.at_death()

    def weapon_is_equipped(self, caller):
        is_equipped = equipped_check(self.caller, "weapon")
        return is_equipped[0]

    def get_attack_weapon(self, caller):
        if self.weapon_is_equipped(caller):
            attack_weapon = caller.db.slots["weapon"]
        else:
            attack_weapon = "your fists"
        return attack_weapon

    def get_attack_attribute(self):
        caller = self.caller
        # To engage in combat you must have declared a class
        if not caller.db.charclass:
            caller.msg("You should pick a class before you go picking fights! (Talk to Caroline at Shieldmaiden's)")
            return

        attack_attr = caller.db.primary_ability
        return attack_attr

    def weapon_type(self, weapon):
        if weapon == "your fists":
            return None

        if not weapon.db.weapon_type:
            return None

        return weapon.db.weapon_type

    # Your weapon will do more for you if you know how to use it
    def proficiency_bonus(self, weapon, weapon_type, attack_attr):
        if weapon_type and weapon.governing_abilities[weapon_type] == attack_attr:
            bonus = round(weapon.db.damage * (random.uniform(1.80, 2.30)))
        else:
            bonus = weapon.db.damage
        return bonus

    def get_attack_score(self, weapon, weapon_type, attack_attr):
        caller = self.caller
        attr_val = caller.attributes.get(attack_attr)

        # Knowing your attack attribute and the weapon equipped, find if it has a buff
        if weapon == "your fists":
            attack_score = caller.db.strength
        else:
            bonus = self.proficiency_bonus(weapon, weapon_type, attack_attr)
            attack_score = attr_val + bonus

        # If your stance is set to aggressive you gain an additional 10% attack advantage
        stance = self.caller.db.stance
        if stance == "aggressive":
            attack_score *= (1.1)
        return attack_score

    def get_defense_score(self, target):
        is_equipped = equipped_check(target, "armor")
        if is_equipped[0] is True:
            slots = target.db.slots
            defense_bonus = slots["armor"].db.defense_bonus or 0
        else:
            defense_bonus = 0
        defense_score = target.db.defense + defense_bonus
        return defense_score

    # Characters in a defensive or evasive stance can make a DC20 "saving throw" to avoid damage altogether
    def damage_avoided(self, stat):
        # Rolls are adjusted up or down based on governing stats
        dice_roll = DiceRoll(stat, pass_dc=20)
        outcome = dice_roll.roll()
        passed = outcome[0]
        return passed

    def message(self, target, dealt_damage, stance, weapon, weapon_type, passed):
        if not target:
            self.caller.msg("You test your might... You attack the air with your " +
                            str(weapon) +
                            " for an attack score of " +
                            str(dealt_damage))
            return

        if passed and stance == "defensive":
            message = str(target) + " blocks and takes no damage!"
        elif passed and stance == "evasive":
            message = str(target) + " dodges and takes no damage!"
        elif weapon and weapon_type and weapon.governing_abilities[weapon_type] == "magic":
            message = (
                           str(self.caller) +
                           random.choice(self.magic_attack_strings) +
                           str(target) + " for " + str(dealt_damage) + " damage"
                           )
        elif dealt_damage and dealt_damage > 0:
            message = str(self.caller) + " attacked " + str(target) + " for " + str(dealt_damage)
            if not utils.inherits_from(self.caller, 'typeclasses.characters.NPC'):
                message += " with your " + str(weapon)
            else:
                message
        elif dealt_damage is not None and dealt_damage <= 0:
            message = str(target) + " shrugs off an attack from " + str(self.caller)
        return message

    def resolve_attack(self, defense_score, attack_score, weapon, weapon_type, target):
        dealt_damage = attack_score - defense_score

        # If your stance is evasive or defensive you have a chance to avoid damage
        stance = target.db.stance
        passed = False
        if stance == "evasive":
            stat = target.db.dex
            passed = self.damage_avoided(stat)
        if stance == "defensive":
            stat = target.db.defense
            passed = self.damage_avoided(stat)
        if passed:
            dealt_damage = 0
        if dealt_damage is not None and dealt_damage > 0:
            XP(self.caller, 30)
        return dealt_damage, self.message(target, dealt_damage, stance, weapon, weapon_type, passed)
