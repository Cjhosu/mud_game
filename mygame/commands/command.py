import random
import evennia
from evennia import Command as BaseCommand, create_object
from typeclasses.characters import Character
"""
Commands

Commands describe the input the account can do to the game.

"""


# from evennia import default_cmds


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

    pass


# -------------------------------------------------------------
#
#  The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
# -------------------------------------------------------------

# from evennia.utils import utils
#
#
# class MuxCommand(Command):
#     """
#     This sets up the basis for a MUX command. The idea
#     is that most other Mux-related commands should just
#     inherit from this and don't have to implement much
#     parsing of their own unless they do something particularly
#     advanced.
#
#     Note that the class's __doc__ string (this text) is
#     used by Evennia to create the automatic help entry for
#     the command, so make sure to document consistently here.
#     """
#     def has_perm(self, srcobj):
#         """
#         This is called by the cmdhandler to determine
#         if srcobj is allowed to execute this command.
#         We just show it here for completeness - we
#         are satisfied using the default check in Command.
#         """
#         return super().has_perm(srcobj)
#
#     def at_pre_cmd(self):
#         """
#         This hook is called before self.parse() on all commands
#         """
#         pass
#
#     def at_post_cmd(self):
#         """
#         This hook is called after the command has finished executing
#         (after self.func()).
#         """
#         pass
#
#     def parse(self):
#         """
#         This method is called by the cmdhandler once the command name
#         has been identified. It creates a new set of member variables
#         that can be later accessed from self.func() (see below)
#
#         The following variables are available for our use when entering this
#         method (from the command definition, and assigned on the fly by the
#         cmdhandler):
#            self.key - the name of this command ('look')
#            self.aliases - the aliases of this cmd ('l')
#            self.permissions - permission string for this command
#            self.help_category - overall category of command
#
#            self.caller - the object calling this command
#            self.cmdstring - the actual command name used to call this
#                             (this allows you to know which alias was used,
#                              for example)
#            self.args - the raw input; everything following self.cmdstring.
#            self.cmdset - the cmdset from which this command was picked. Not
#                          often used (useful for commands like 'help' or to
#                          list all available commands etc)
#            self.obj - the object on which this command was defined. It is often
#                          the same as self.caller.
#
#         A MUX command has the following possible syntax:
#
#           name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#         The 'name[ with several words]' part is already dealt with by the
#         cmdhandler at this point, and stored in self.cmdname (we don't use
#         it here). The rest of the command is stored in self.args, which can
#         start with the switch indicator /.
#
#         This parser breaks self.args into its constituents and stores them in the
#         following variables:
#           self.switches = [list of /switches (without the /)]
#           self.raw = This is the raw argument input, including switches
#           self.args = This is re-defined to be everything *except* the switches
#           self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                      no = is found, this is identical to self.args.
#           self.rhs: Everything to the right of = (rhs:'right-hand side').
#                     If no '=' is found, this is None.
#           self.lhslist - [self.lhs split into a list by comma]
#           self.rhslist - [list of self.rhs split into a list by comma]
#           self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#           All args and list members are stripped of excess whitespace around the
#           strings, but case is preserved.
#         """
#         raw = self.args
#         args = raw.strip()
#
#         # split out switches
#         switches = []
#         if args and len(args) > 1 and args[0] == "/":
#             # we have a switch, or a set of switches. These end with a space.
#             switches = args[1:].split(None, 1)
#             if len(switches) > 1:
#                 switches, args = switches
#                 switches = switches.split('/')
#             else:
#                 args = ""
#                 switches = switches[0].split('/')
#         arglist = [arg.strip() for arg in args.split()]
#
#         # check for arg1, arg2, ... = argA, argB, ... constructs
#         lhs, rhs = args, None
#         lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#         if args and '=' in args:
#             lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#             lhslist = [arg.strip() for arg in lhs.split(',')]
#             rhslist = [arg.strip() for arg in rhs.split(',')]
#
#         # save to object properties:
#         self.raw = raw
#         self.switches = switches
#         self.args = args.strip()
#         self.arglist = arglist
#         self.lhs = lhs
#         self.lhslist = lhslist
#         self.rhs = rhs
#         self.rhslist = rhslist
#
#         # if the class has the account_caller property set on itself, we make
#         # sure that self.caller is always the account if possible. We also create
#         # a special property "character" for the puppeted object, if any. This
#         # is convenient for commands defined on the Account only.
#         if hasattr(self, "account_caller") and self.account_caller:
#             if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                 # caller is an Object/Character
#                 self.character = self.caller
#                 self.caller = self.caller.account
#             elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                 # caller was already an Account
#                 self.character = self.caller.get_puppet(self.session)
#             else:
#                 self.character = None


class CmdSetCharClass(Command):
    key = "become"
    def func(self):
        "This is the class choice function"
        errmsg = "You must pick a valid class (Ranger, Warrior, Mage, Druid, Rogue, Paladin)"
        self.caller.at_object_creation()
        if not self.args:
            self.caller.msg(errmsg)
            return
        charclass = str(self.args.strip())
        self.caller.db.charclass = charclass
        if charclass == 'Ranger':
            self.caller.db.strength *= .65
            self.caller.db.magic *= .70
            self.caller.db.dex *= 1.35
            self.caller.db.intel *= 1.2
            self.caller.db.luck *= 1.1
            self.caller.msg("I can smell the woods on ya, not in a bad way mind you, just a faint musk!")

        elif charclass == 'Warrior':
            self.caller.db.strength *= 1.80
            self.caller.db.magic *= .45
            self.caller.db.dex *= 1.05
            self.caller.db.intel *= .60
            self.caller.db.luck *= 1.1
            self.caller.msg("I should have been able to tell by the muscles!")

        elif charclass == 'Mage':
            self.caller.db.strength *= 1.80
            self.caller.db.magic *= .45
            self.caller.db.dex *= 1.05
            self.caller.db.intel *= .60
            self.caller.db.luck *= 1.1
            self.caller.msg("Spells for days son!")

        elif charclass == 'Druid':
            self.caller.db.strength *= .70
            self.caller.db.magic *= 1.20
            self.caller.db.dex *= 1.15
            self.caller.db.intel *= 1.05
            self.caller.db.luck *= .90
            self.caller.msg("Ah, Blessed be")

        elif charclass == 'Rogue':
            self.caller.db.strength *= 1.15
            self.caller.db.magic *= .45
            self.caller.db.dex *= 1.25
            self.caller.db.intel *= .95
            self.caller.db.luck *= 1.2
            self.caller.msg("That's fine, try not to steal anything.")

        elif charclass == 'Paladin':
            self.caller.db.strength *= 1.50
            self.caller.db.magic *= 1.05
            self.caller.db.dex *= .85
            self.caller.db.intel *= .60
            self.caller.db.luck *= 1.0
            self.caller.msg("I see you follow the righteous path")

class CmdEquip(Command):
    key = "equip"

    def func(self):
        caller = self.caller
        if not caller.db.slots:
            caller.db.slots = {"armor" : '', "weapon":'' }
        slots = caller.db.slots
        if not self.args:
            caller.msg("You have "+ str(slots)+ " equipped")
        else:
            args = self.args.strip()
            item = caller.search(args, candidates=caller.contents,nofound_string='Wat')
            if item.is_typeclass('typeclasses.objects.Weapon'):
                caller.msg("that is a weapon with a damage value of " + str(item.db.damage))
                slots["weapon"] = item
            else:
                caller.msg("Cant")

class CmdAttack(Command):
    """
    issues an attack

    Usage: +attack

    This will calculate a new combat score based on your Strength.
    Your combat score is visible to everyone in the same location
    """

    key = "+attack"
    help_category = "mush"
    attack_attr_dict = {"Ranger" : "dex", "Warrior" : "strength", "Mage" : "magic"}

    def func(self):
        "Calculate an attack based on class and weapon"
        caller = self.caller
        slots = caller.db.slots

        #What attribute do you use to attack?
        attack_attr =  self.get_attack_attribute()

        #If you have an equipped weapon attack with it...
        if slots["weapon"]:
            attack_weapon = slots["weapon"]
            attack_score = self.get_attack_score(attack_weapon,attack_attr)

        #Otherwise use your fists
        else:
            attack_weapon = "your fists"
            attack_score = round(random.uniform(1.0,1.5)* strength)

        #save most recently computed attack
        caller.db.attack_score = attack_score

        #handle messaging
        message = "%s +attack%s with %s for a combat score of %s!"
        caller.msg(message % ("You", "",attack_weapon, attack_score))
        caller.location.msg_contents(message % (caller.key, "s", attack_weapon, attack_score), exclude=caller)

    def get_attack_attribute(self):
        caller = self.caller
        charclass = caller.db.charclass
        #find your favored attribute based on your class
        attack_attr = self.attack_attr_dict[charclass]
        return attack_attr

    def weapon_multiplier(self,weapon, attack_attr):
        #Your weapon will do more for you if you know how to use it
        caller=self.caller
        multiplier = round(weapon.db.damage * (random.uniform(1.0,1.5)))
        if weapon.db.weapon_type == 'melee' and attack_attr == 'strength':
            multiplier
        elif weapon.db.weapon_type == 'ranged' and attack_attr == 'dex':
            multiplier
        else:
            multiplier = weapon.db.damage
        return multiplier

    def get_attack_score(self, weapon, attack_attr):
        caller = self.caller
        attr_val = caller.attributes.get(attack_attr)
        #knowing you attack attribute and the weapon equipped find if it has a buff
        multiplier = self.weapon_multiplier(weapon, attack_attr)
        attack_score = attr_val + multiplier
        return attack_score

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
        npc = create_object("characters.Character",
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


