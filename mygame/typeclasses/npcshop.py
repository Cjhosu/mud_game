from evennia.utils import evmenu
from evennia import Command, DefaultRoom, DefaultExit, DefaultObject
from evennia.utils.create import create_object
from evennia import CmdSet
from typeclasses.rooms import Room

def menunode_shopfront(caller):

    shopname = caller.location.key
    wares = caller.location.db.storeroom.contents

    #Wares includes everything in the storeroom including the door.  Dont sell the door

    wares = [ware for ware in wares if ware.key.lower() != "door"]

    text = "*** Welcome to %s! ***\n" % shopname
    if wares:
        text += " Things for sale (choose 1-%i to inspect);"\
                " quit to exit:" %len(wares)
    else:
        text += "  There is nothing for sale; quit to exit"

    options = []

    for ware in wares:
        options.append({"desc": "%s (%s gold)" %
                           (ware.key, ware.db.gold_value or 1),
                           "goto" : "menunode_inspect_and_buy"})

    return text, options


class NPCShop(Room):
    def at_object_creation(self):
        self.cmdset.add_default(ShopCmdSet)
        self.db.storeroom = None

def menunode_inspect_and_buy(caller, raw_string):

    wares = caller.location.db.storeroom.contents
    wares = [ware for ware in wares if ware.key.lower() != "door"]
    iware = int(raw_string) -1
    ware = wares[iware]
    value = ware.db.gold_value or 1
    wealth = caller.db.gold or 0
    text = "You inspect %s:\n\n%s" % (ware.key, ware.db.desc)

    def buy_ware_result(caller):

        if wealth >= value:
            rtext = "you pay %i gold and purchase %s!" % \
                           (value, ware.key)
            caller.db.gold -= value
            ware.move_to(caller, quiet = True)
        else:
            rtext = "You cannot afford %i gold for %s!" % \
                    (value, ware.key)
        caller.msg(rtext)

    options = ({"desc": "Buy %s for %s gold" %\
                    (ware.key, ware.db.gold_value or 1),
                "goto": "menunode_shopfront",
                "exec": buy_ware_result},
                 {"desc": "Look for something else",
                   "goto": "menunode_shopfront"})

    return text, options

class CmdBuy(Command):
    key = "buy"
    aliases = ("shop", "kaufen")

    def func(self):
        evmenu.EvMenu(self.caller, "typeclasses.npcshop", startnode="menunode_shopfront")

class ShopCmdSet(CmdSet):
    def at_cmdset_creation(self):
        self.add(CmdBuy())

# command to build a complete shop (the Command base class
# should already have been imported earlier in this file)
class CmdBuildShop(Command):
    """
    Build a new shop

    Usage:
    @buildshop shopname

    This will create a new NPCshop room
    as well as a linked store room (named
    simply <storename>-storage) for the
    wares on sale. The store room will be
    accessed through a locked door in
    the shop.
    """
    key = "@buildshop"
    locks = "cmd:perm(Builders)"
    help_category = "Builders"

    def func(self):
        "Create the shop rooms"
        if not self.args:
            self.msg("Usage: @buildshop <storename>")
            return
        # create the shop and storeroom
        shopname = self.args.strip()
        shop = create_object(NPCShop,
                            key=shopname,
                              location=None)
        storeroom = create_object(Room,
                                  key="%s-storage" % shopname,
                                  location=None)
        shop.db.storeroom = storeroom
        # create a door between the two
        shop_exit = create_object(DefaultExit,
                                key="back door",
                                aliases=["storage", "store room"],
                                location=shop,
                                destination=storeroom)
        storeroom_exit = create_object(DefaultExit,
                                        key="door",
                                        location=storeroom,
                                        destination=shop)
        # make a key for accessing the store room
        storeroom_key_name = "%s-storekey" % shopname
        storeroom_key = create_object(DefaultObject,
                                    key=storeroom_key_name,
                                    location=shop)
        # only allow chars with this key to enter the store room
        shop_exit.locks.add("traverse:holds(%s)" % storeroom_key_name)

        # inform the builder about progress
        self.caller.msg("The shop %s was created!" % shop)
