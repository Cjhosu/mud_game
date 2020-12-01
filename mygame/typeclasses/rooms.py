"""
Room
Rooms are simple containers that has no location of their own.
"""
from evennia import DefaultRoom, utils

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

class EnemyRoom(Room):

    def at_object_receive(self, obj, source_location):
        if not utils.inherits_from(obj, 'typeclasses.characters.NPC') and utils.inherits_from(obj, 'typeclasses.characters.Character'):
            obj.execute_cmd('look')
            for item in self.contents:
                if utils.inherits_from(item, 'typeclasses.characters.NPC'):
                    item.at_char_entered(obj)
