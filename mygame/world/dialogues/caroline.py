
def menu_start_node(caller):
    text = "'Hey there! How can I help you today?'"

    options = (
            {"desc": "Hi there I am new and would like some information!", "goto" : "info1"},
            {"desc": "Nevermind", "goto" : "END"}
            )

    return text, options

def info1(caller):
    text = "'Welcome to our little nook of sunshine!  Most folks come around here to visit Daryl's shop or declare their professions.  Can I tell you about either those things?'"

    options = (
            {"desc" : "I'd like to learn about professions.", "goto" : "info2"},
            {"desc" : "Tell me more about Daryl's shop.", "goto" : "info3"},
            {"desc" : "I think I am good for now.", "goto" : "END"}
            )

    return text, options

def info2(caller):
    text = "'It is good that you've come to such a land of opportunity where you can be whatever you want ... as long as it is one of six classes.'"

    options = ({"desc" : "Sounds great, I am ready to choose!", "goto" : "info4"},
               {"desc" : "I'd like to hear about Daryl's shop", "goto" : "info3"},
               {"desc" : "Let me think about it some more.", "goto" : "END"}
              )

    return text, options

def info3(caller):
    text = "'If you head out the exit on the east side of the building and down the garden path you'll see Daryl's workshop.  He is awlays tinkering with something, and he usually has some things to sell.'"

    options = (
            {"desc" : "Great I'll visit Daryl now.", "goto" : "END"},
            {"desc" : "I'd like to learn about professions.", "goto" : "info2"},
            {"desc" : "Those are all the questions I have for now.", "goto" : "END"}
            )

    return text, options

def info4(caller):
    text = "'What would you like your profession to be?'"

    options = (
            {"key": "Ranger",
             "desc": "Primary attribute is dex, lower strength and magic",
             "goto": (set_char_class, {"attr": "Ranger"})},

            {"key": "Warrior",
             "desc": "Primary attribute is strength, lower intel and magic",
             "goto": (set_char_class, {"attr": "Warrior"})},

            {"key": "Mage",
             "desc": "Primary attribute is magic, lower strength and dex",
             "goto": (set_char_class, {"attr": "Mage"})},

            {"key": "Druid",
             "desc": "Primary attribute is magic, most balanced profession",
             "goto": (set_char_class, {"attr": "Druid"})},

            {"key": "Rogue",
             "desc": "Primary attribute is dex, lower magic otherwise balanced ",
             "goto": (set_char_class, {"attr": "Rogue"})},

            {"key": "Paladin",
             "desc": "Primary attribute is strength, lower intel otherwise balanced",
             "goto": (set_char_class, {"attr": "Paladin"})}
            )

    return text, options

def set_char_class(caller, raw_string, **kwargs):
    attrname = kwargs.get("attr")
    caller.at_object_creation()
    caller.db.charclass = attrname
    return attrname

def Ranger(caller):
    caller.db.strength *= .65
    caller.db.magic *= .70
    caller.db.dex *= 1.35
    caller.db.intel *= 1.2
    caller.db.luck *= 1.1
    caller.msg("\n I can smell the woods on ya, not in a bad way mind you, just a faint musk!")
    return

def Warrior(caller):
    caller.db.strength *= 1.80
    caller.db.magic *= .45
    caller.db.dex *= 1.05
    caller.db.intel *= .60
    caller.db.luck *= 1.1
    caller.msg("\n I should have been able to tell by the muscles!")
    return

def Mage(caller):
    caller.db.strength *= .45
    caller.db.magic *= 1.70
    caller.db.dex *= .75
    caller.db.intel *= 1.0
    caller.db.luck *= 1.1
    caller.msg("\n Spells for days son!")
    return

def Druid(caller):
    caller.db.strength *= .70
    caller.db.magic *= 1.30
    caller.db.dex *= 1.05
    caller.db.intel *= 1.05
    caller.db.luck *= .90
    caller.msg("\n Ah, Blessed be")
    return

def Rogue(caller):
    caller.db.strength *= 1.00
    caller.db.magic *= .50
    caller.db.dex *= 1.35
    caller.db.intel *= .95
    caller.db.luck *= 1.2
    caller.msg("\n That's fine, try not to steal anything.")
    return

def Paladin(caller):
    caller.db.strength *= 1.50
    caller.db.magic *= 1.05
    caller.db.dex *= .85
    caller.db.intel *= .60
    caller.db.luck *= 1.0
    caller.msg("\n I see you follow the righteous path")
    return

def END(caller):
    text = "'Ok Bye!'"

    options = ()

    return text, options

