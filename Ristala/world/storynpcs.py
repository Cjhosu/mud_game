"""
Npcs that drive the story

@create/drop John : contrib.talking_npc.TalkingNPC
"""
from commands.command import Command, CmdCreateNPC
from evennia import DefaultObject, CmdSet, default_cmds
from evennia.utils.evmenu import EvMenu
from typeclasses.characters import NPC


class CmdTalk(Command):

    key = "talk"
    aliases = ["talk to"]
    locks = "cmd:all()"
    help_category = "General"


    def func(self):

        caller = self.caller
        if not self.args:
            caller.msg("To whom are you trying to talk")
        else:
            args = self.args.strip().lower()
            try:
                EvMenu(self.caller, "world.dialogues."+args, startnode="menu_start_node")
            except:
                caller.msg("That is not someone you can talk to.")

class TalkingCmdSet(CmdSet):
    key = "talkingcmdset"

    def at_cmdset_creation(self):
        self.add(CmdTalk())
