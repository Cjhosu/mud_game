from world.magic.spells import *
class SpellFactory():

    spell_data_dict = {
            "shield" : "Shield",
            "magic missile" : "MagicMissile",
            "firebolt" : "Firebolt"
        }

    def get_spell_instc(self, caller, spell_name, target_list):
        try:
            cls = globals()[self.spell_data_dict[spell_name]]
        except:
            cls = globals()["Spell"]
        spl_instc = cls(caller, spell_name, target_list) 
        return (spl_instc)

