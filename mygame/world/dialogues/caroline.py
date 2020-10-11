
def menu_start_node(caller):
    text = "'Hey there! How can I help you today?'"

    options = (
            {"desc": "Hi there I am new and would like some information!", "goto" : "info1"},
            {"desc": "Nevermind", "goto" : "END"},
            )

    return text, options

def info1(caller):
    text = "'Welcome to our little nook of sunshine!  Most folks come around here to visit Daryl's shop or declare their professions.  Can I tell you about either those things'"

    options = (
            {"desc" : "I'd like to learn about professions.", "goto" : "info2"},
            {"desc" : "Tell me more about Daryl's shop.", "goto" : "info3"},
            {"desc" : "I think I am good for now.", "goto" : "END"}
            )

    return text, options

def info2(caller):
    text = "'It is good that you've come to such a land of opportunity where you can be whatever you want ... as long as it is one of six classes.  When we are done talking just announce it to the room. (say something like 'become Warrior')'"

    options = (
            {"desc" : "Sounds great, I am ready to choose!", "goto" : "END"},
            {"desc" : "I'd like to hear about Daryl's shop", "goto" : "info3"},
            {"desc" : "Let me think about it some more.", "goto" : "END"}
            )

    return text, options

def info3(caller):
    text = "'If you head out the exit on the west side of the building and down the garden path you'll see Daryl's workshop.  He is awlays tinkering with something, and he usually has some things to sell.'"

    options = (
            {"desc" : "Great I'll visit Daryl now.", "goto" : "END"},
            {"desc" : "I'd like to learn about professions.", "goto" : "info2"},
            {"desc" : "Those are all the questions I have for now.", "goto" : "END"}
            )

    return text, options

def END(self, caller):
    text = "'Ok Bye'!"

    options = ()

    return text, options

