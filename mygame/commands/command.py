import evennia
import time
from evennia import Command as BaseCommand, DefaultRoom, DefaultExit, DefaultObject
from evennia.utils.create import create_object
from evennia.utils import evtable
from typeclasses.characters import Character, NPC
from world.combat.combat import CombatHandler

"""
Commands

Commands describe the input the account can do to the game.

"""
class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_cmd(): If this returns anything truthy, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_cmd(): Extra actions, often things done after
            every command, like prompts.

    """
    def at_post_cmd(self):
        super().at_post_cmd()
        caller = self.caller
        prompt = "HP:%i/%i  Level:%i  XP:%i/%i" % (caller.db.health, caller.db.max_health, caller.db.level, caller.db.xp, caller.db.next_level_xp)
        caller.msg(prompt=prompt)

    pass

class CmdEquip(Command):
    key = "equip"

    def func(self):
        caller = self.caller
        if not caller.db.slots:
            caller.db.slots = {"armor" : None, "weapon":None }
        slots = caller.db.slots
        if not self.args:
            caller.msg("You have "+ str(slots)+ " equipped")
        else:
            args = self.args.strip()
            item = caller.search(args, candidates=caller.contents,nofound_string= args +" doesn't seem to be something you are carrying")
            if item:
                if item.is_typeclass('typeclasses.objects.Weapon'):
                    slots["weapon"] = item
                    caller.msg("You have equipped "+ str(item) +" to your weapon slot, it has a damage value of " + str(item.db.damage))
                elif item.is_typeclass('typeclasses.objects.Armor'):
                    slots["armor"] = item
                    caller.msg("You have equipped " + str(item) + " to your armor slot it has a defense bonus of " + str(item.db.defense_bonus))
                else:
                    caller.msg("That item is not equipable")


class CmdCreateNPC(Command):
    """
    create a new npc

    Usage:
        +createNPC <name>
    """

    key = "+createnpc"
    aliases = ["+createNPC"]
    locks = "call:not perm(nopcs)"
    help_category = "mush"

    def func(self):
        #creates an object and names it
        caller = self.caller
        if not self.args:
            caller.msg("Usage: +createNPC <name>")
            return
        if not caller.location:
            #you can't create a npc if you are out of character
            caller.msg("You must have a location to create an npc")
            return
        name = self.args.strip().capitalize()
        npc = create_object("characters.NPC",
                             key=name,
                             location=caller.location,
                             locks="edit:id(%i) and perm(Builders);call:false()" % caller.id)
        #announce
        message = "%s created the NPC '%s'."
        caller.msg(message % ("You", name))
        caller.location.msg_contents(message % (caller.key, name), exclude=caller)

class CmdEditNPC(Command):
    """
    edit an existing NPC

    Usage:
      +editnpc <name>[/atribute> [=value]]

    Examples:
    +editnpc mynpc/health = 5 - sets health to 5
    +editnpc mynpc/health  - displays health value
    +editnpc mynpc - displays attributes you can edit

    ths command edxits an existing NPC.  You must have permissions to edit this npc.

    """
    key = "+editnpc"
    aliases = ["+editNPC"]
    locks = "cmd:not perm(nonpcs)"
    help_category = "mush"

    def parse(self):
        "We need to do some parsing here"
        args = self.args
        propname, propval = None, None
        if "=" in args:
            args, propval = [part.strip() for part in args.rsplit("=",1)]
        if "/" in args:
            args, propname = [part.strip() for part in args.rsplit("/", 1)]
        # store, so we can access it below in sie func()
        self.name = args
        self.propname = propname
        # a propval without a propname is meaningless
        self.propval = propval if propname else None

    def func(self):
        # do the editing

        allowed_propnames = ("health", "strength", "dex", "intel", "luck", "magic")

        caller = self.caller
        if not self.args or not self.name:
            caller.msg("Usage: +editnpc name[/propname][=propval]")
            return
        npc = caller.search(self.name)
        try:
            if not npc.access(caller, "edit"):
                caller.msg("You cannot change this NPC")
                return
        except:
            caller.msg("Who dat?")
            return
        if not self.propname:
            # based on our examples this mean we just list stats
            output = f"Properties of {npc.key}:"
            for propname in allowed_propnames:
                output += f"\n {propname} = {npc.attributes.get(propname, default = 'N/A')}"
            caller.msg(output)
        elif self.propname not in allowed_propnames:
            caller.msg(f"You may only change {',' .join(allowed_propnames)}.")
        elif self.propval:
            # assigning a new propvalue
            # in this example, the properties are all integers...
            intpropval = int(self.propval)
            npc.attributes.add(self.propname, intpropval)
            caller.msg(f"You've set {npc.key}'s {self.propname} property to {npc.attributes.get(self.propname, default = 'N/A')}")
        else:
            # propname set, but not propval - show the current value
            caller.msg(f"{npc.key} has property {self.propname} = {npc.attributes.get(self.propname, default = 'N/A')}")

class CmdAttack(Command):
    """
    issues an attack

    Usage: +attack

    This will calculate a new combat score based on your Strength.
    Your combat score is visible to everyone in the same location
    """

    key = "+attack"
    help_category = "mush"

    def func(self):
        caller = self.caller
        now = time.time()
        if hasattr(self, "lastattack") and now - self.lastattack < 5 :
            caller.msg("Your attack is on cooldown")
            return
        cmbt = CombatHandler()
        "parse target"
        if self.args:
            target = self.args.strip()
            cmbt.target = target
        else:
            target = None
        cmbt.caller = caller
        cmbt.init_combat(caller, target)
        self.lastattack = now

class CmdShowAttr(Command):

    """
     prints the main character attribute in a table

    Usage: mystats

    """
    key = 'mystats'
    help_category = "mush"

    def func(self):
        caller = self.caller
        charclass = caller.db.charclass
        defense = round(caller.db.defense)
        health = round(caller.db.health)
        intel = round(caller.db.intel)
        luck = round(caller.db.luck)
        magic = round(caller.db.magic)
        strength = round(caller.db.strength)
        dex = round(caller.db.dex)
        attr_points = caller.db.attr_points

        table = evtable.EvTable("Attribute", "Value",
                table = [["charclass", "defense","health","intel","luck", "magic","dex", "strength", "upgrade points"],
                [charclass, defense, health, intel, luck, magic, dex, strength, attr_points]])
        caller.msg(table)

class CmdSetStance(Command):

    """
    sets the players stance to aggressive, defensive, or evasive

    Usage:
      +set stance <stance option>

    Examples:
    +set stance evasive
    """

    key = '+set stance'
    help_category = "mush"

    def func(self):
        caller = self.caller
        err_msg = "Usage: +set stance [aggressive]|[defensive]|[evasive]"
        if not self.args:
            caller.msg(err_msg)
            return
        else:
            args = self.args.strip()
        if args not in ("aggressive","defensive","evasive"):
            caller.msg(err_msg)
        else:
            caller.db.stance = args
            caller.msg("Your stance has been set to " + args)

