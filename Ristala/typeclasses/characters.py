import random
from evennia.utils import interactive
from world.helpers import display_prompt, drop_gold_pieces
from evennia import TICKER_HANDLER, create_object
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
        self.db.gold = 0
        TICKER_HANDLER.add(10, self.at_prompt)

    def at_prompt(self):
        display_prompt(self)

    def at_after_move(self, source_loaction):
        """
        The default of this function calls "look" when a character enter a room.
        This is overwritten in the default room typeclass so look is always called·
        before an NPC interaction is triggered.
        """
        #self.execute_cmd('look')
        pass

    @interactive
    def at_death(self):
        self.location.msg_contents(str(self)+ " has lost the will to live")
        yield 3
        self.msg("Re-Spawning you somewhere cozy")
        yield 2
        self.msg("Try to stay alive.")
        yield 2
        self.move_to(self.home, quiet = True)
        self.db.health = self.db.max_health

class NPC(Character):

    def at_object_creation(self):
        self.db.charclass = 'Warrior'
        super(NPC, self).at_object_creation()

    @interactive
    def at_char_entered(self, character):

        #Called only when a character enters a special room typeclass
        if self.db.hostile:
            character.location.msg_contents(str(self) +' is giving you some serious side-eye')

            #Give the player some time to react
            yield random.randint(10,20)

            #Attack if both parties are alive
            while self.db.health > 0 and character.db.health > 0:
                self.execute_cmd(f"+attack {character}")

                #Randomize attack timing a bit
                yield random.randint(10,20)

        #Friendly NPCs just say whats up
        else:
            self.execute_cmd(f"say Greetings, {character}!")

    @interactive
    def at_death(self):
    #Enemies dying is a bit different than player characters dying

        self.location.msg_contents(str(self)+ " has lost the will to live")
        number = drop_gold_pieces()
        loot = create_object(
                typeclass = 'typeclasses.objects.Gold',
                key = str(number) +' gold',
                location = self.location)

        loot.attributes.add('value', number)
        self.location.msg_contents(str(self)+ " dropped " + str(loot))

        "Take the enemy out of play for 60 seconds"
        self.move_to(None, to_none = True)
        yield 30

        "Re-spawn them"
        self.move_to(self.home, quiet = True)
        self.db.health = self.db.max_health
