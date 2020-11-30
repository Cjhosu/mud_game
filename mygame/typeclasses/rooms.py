"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom, utils
from commands.default_cmdsets import ChargenCmdset

class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def at_object_receive(self, obj, source_location):
        if not utils.inherits_from(obj, 'typeclasses.characters.NPC') and utils.inherits_from(obj, 'typeclasses.characters.Character'):
            obj.execute_cmd('look')

    pass

class ChargenRoom(Room):
    #This room class is used by character-generation rooms.
    #It makes the ChargenCmdSet available.

    def at_object_creation(self):
        "This is called only on creation"
        self.cmdset.add(ChargenCmdset, permanent=True)
"""
    def return_appearance(self, looker):
        The return from this method is what looker sees when looking at this object
        text = super().return_appearance(looker)
        return text
        """

class EnemyRoom(Room):
    pass

