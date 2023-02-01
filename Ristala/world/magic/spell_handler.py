from evennia import utils
from world.helpers import equipped_check, get_num_dice, DiceRoll
from world.rules.levels import XP
import random

class SpellHandler():

    def __init__(self, caller, spell_name, target_list):
        self.caller = caller
        self.spell_name = spell_name.strip()
        self.target_list = target_list or self.caller

    def init_spell(self):
        spell_name = getattr(self, self.spell_name, self.no_spell)
        return spell_name()

    def no_spell(self):
        self.caller.msg("That doesn't seem to be a real spell")

    def shield(self):
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )
