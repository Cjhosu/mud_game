from world.magic.spell_factory import SpellFactory

class SpellHandler():

    def __init__(self, caller, spell_name, target_list):
        self.caller = caller
        self.spell_name = spell_name.strip()
        self.target_list = target_list or self.caller

    def init_spell(self):
        spell_name = self.spell_name.lower()
        if spell_name == None:
            spell_name == ''
        spell = SpellFactory.get_spell_instc(self.caller, spell_name, self.target_list)
        if spell.has_enough_mana():
            spell.action()
        else:
            self.caller.msg("You don't have enough mana to do that")
            self.caller.msg("The current mana level is " + str(self.caller.db.mana) + " the cost to cast is " + str(spell.mana_cost))

