
class Spell():

    def __init__(self, caller, spell_name, target_list):
        self.caller = caller
        self.spell_name = spell_name.strip()
        self.target_list = target_list or self.caller

    def has_enough_mana(self):
        try:
            return self.mana_cost <= self.caller.db.mana
        except:
            return True

    def action(self):
        self.caller.msg("Check the spellbook again, " + str(self.spell_name) + " doesn't seem to be a spell")

class Firebolt(Spell):

    mana_cost = 25

    def action(self):
        self.caller.db.mana -= self.mana_cost
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )

class Shield(Spell):

    mana_cost = 30

    def action(self):
        self.caller.db.mana -= self.mana_cost
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )

class MagicMissile(Spell):

    mana_cost = 35

    def action(self):
        self.caller.db.mana -= self.mana_cost
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )
