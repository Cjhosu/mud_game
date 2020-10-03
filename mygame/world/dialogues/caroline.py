
def menu_start_node(caller):
    text = "'Hey there you're looking pretty green!  First time in the magical land of MagicLand?'"

    options = (
            {"desc": "No, we spoke just the other day", "goto" : "END"},
            {"desc": "Is it that obvious?", "goto": "info1"}
            )

    return text, options

def info1(caller):
    text = "'It is. But hey, welcome to our pub!  We a welcoming bunch here at the end of civilization!  Here in Magicland you can be whatever you want as long as it is one of six classes.  When we are done talking just announce it to the room. (say something like 'become Warrior')'"

    options = (
            {"desc" : "Sounds great, I am ready to choose!", "goto" : "END"},
            {"desc" : "Let me think about it some more.", "goto" : "END"}
            )

    return text, options

def END(self, caller):
    text = "'Ok Bye'!"

    options = ()

    return text, options

