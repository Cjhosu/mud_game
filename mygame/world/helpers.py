


def equipped_check(caller, item):
    slots = caller.db.slots
    caller = str(caller)
    equipped = False

    if slots:
        if slots[item]:
            equipped = True
            message = caller + "has a "+ item + " equipped"
        else:
            message = caller + "has no "+ item + " equipped"
    else :
        message = caller + " has no equipment slots"

    return equipped, message
