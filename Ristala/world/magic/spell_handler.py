
class SpellHandler():

    def __init__(self, caller, spell_name, target_list):
        self.caller = caller
        self.spell_name = spell_name.strip()
        self.target_list = target_list or self.caller

    def init_spell(self):
        spell_name = self.spell_name.lower()
        if spell_name == None or spell_name == '':
            self.no_spell()
        else:
            try:
                spell_data = SpellFactory(spell_name)
                cls, cost = spell_data.get_spell_data()[0:2]
                spell = cls(self.caller, self.spell_name, self.target_list)
                self.caller.msg("The current mana_level is " + str(self.caller.db.mana) + " the cost to cast is " + str(cost))
                spell.action()
            except:
                self.no_spell()

    def no_spell(self):
        self.caller.msg("That doesn't seem to be a real spell")

class SpellFactory():
    spell_data = {
            "shield" : ["Shield", 35],
            "magic missile" : ["MagicMissile", 25]
        }

    def __init__(self, spell_name):
        self.spell_name = spell_name

    def get_spell_data(self):
        cls = globals()[self.spell_data[self.spell_name][0]]
        self.mana_cost = self.spell_data[self.spell_name][1]
        return (cls, self.mana_cost)

class Shield(SpellHandler):
    def action(self):
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )

class MagicMissile(SpellHandler):
    def action(self):
        self.caller.msg("You've cast " + str(self.spell_name) +"(" + str(self.target_list) + ")" )
