from world.magic.spells import *

spell_data_dict = {
        "shield" : "Shield",
        "magic missile" : "MagicMissile",
        "firebolt" : "Firebolt"
    }

class SpellFactory():

    def get_spell_instc(caller, spell_name, target_list):
        if not spell_name in spell_data_dict:
            cls = globals()["Spell"]
        else:
            cls = globals()[spell_data_dict[spell_name]]
        spl_instc = cls(caller, spell_name, target_list) 
        return (spl_instc)

