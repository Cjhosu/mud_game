from evennia.utils import interactive

"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter


"""
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

class Character(DefaultCharacter):
    def at_object_creation(self):
        "This is called when the object is first created only."
        self.db.strength = 100
        self.db.magic = 100
        self.db.dex = 100
        self.db.intel = 100
        self.db.luck = 100
        self.db.defense = 100
        self.db.health = 255
        self.db.max_health = 255
        self.db.level = 1
        self.db.xp = 0
        self.db.next_level_xp = 100
        self.db.attr_points = 1

    def at_after_move(self, source_loaction):
        """
        The default of this function calls "look" when a character enter a room.
        This is overwritten in the default room typeclass so look is always called 
        before an NPC interaction is triggered.
        """
        #self.execute_cmd('look')
        pass


class NPC(Character):

    def at_object_creation(self):
        self.db.charclass = 'Warrior'
        super(NPC, self).at_object_creation()

    @interactive
    def at_char_entered(self, character):
        if self.db.hostile:
            character.location.msg_contents(str(self) +' is giving you some serious side-eye')
            yield 20
            self.execute_cmd(f"+attack {character}")
        else:
            self.execute_cmd(f"say Greetings, {character}!")
