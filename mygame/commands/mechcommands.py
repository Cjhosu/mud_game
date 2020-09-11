from evennia import Command
from evennia import CmdSet
from evennia import default_cmds


class CmdShoot(Command):
    """ 
    Firing the mech's gun

    Usage: Shoot [target]

    This will fire your mech's gun. If no target is given, you will shoot in the air.
    """

    key = "shoot"
    aliases = ["fire", "fire!"]

    def func(self):
        "This does the shooting"
        caller = self.caller
        location = caller.location

        if not self.args:
            # no argument given so shoot in the air
            message = "BOOM! The mech fires its gun in the air"
            location.msg_contents(message)
            return

        target = caller.search(self.args.strip())
        if target:
            message = "The mech fires its gun at %s" % target.key
            location.msg_contents(message)
        

class MechCmdSet(CmdSet):
    """
    This allows the mech to do stuff
    """
    key = "mechcmdset"

    def at_cmdset_creation(self):
        "Called once, when cmdset is first created"
        self.add(CmdShoot())
        
