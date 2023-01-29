from evennia import utils
from world.helpers import equipped_check, get_num_dice, DiceRoll
from world.rules.levels import XP
import random

class SpellHandler():

    def __init__(self, caller, spell_name, target_list):
        self.caller = caller
        self.spell_name = spell_name
        self.target_list = target_list

    def init_spell(self):
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )
