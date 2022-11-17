from evennia.utils import evmenu
from evennia import Command, DefaultRoom, DefaultExit, DefaultObject
from evennia.utils.create import create_object
from evennia import CmdSet
from typeclasses.rooms import Room

class NPCShop(Room):
    def at_object_creation(self):
        self.cmdset.add_default(ShopCmdSet)
        self.db.storeroom = None

class CmdBuy(Command):
    key = "shop"
    aliases = ("buy","sell", "kaufen")

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

"""
Below methods are used for interacting with the shop
"""

def menunode_shopfront(caller):

    shopname = caller.location.key

    text = "*** Welcome to %s! ***\n" % shopname

    options = ({"desc": "Buy gear",
                "goto": "menunode_buy_home"},
               {"desc": "Sell gear",
                "goto": "menunode_sell_home"})

    return text, options

def menunode_sell_home(caller):
    shopname = caller.location.key
    inv_items = caller.contents

    text = ""

    if inv_items:
        text += " Things you can sell (choose 1-%i to sell);"\
                " quit to exit:" %len(inv_items)
    else:
        text += "  There is nothing you can sell; quit to exit"

    options = []

    for item in inv_items:
        offer = int(.7*(item.db.value))
        options.append({"desc": "%s (%s gold)" %\
                        (item.key, offer or 1),
                        "exec" : ("menunode_sell", {"item" : item, "offer" : offer}),
                        "goto": "menunode_shopfront"})

    options.append({"desc": "Go back",
                        "goto": "menunode_shopfront"})

    return text, options

def menunode_sell(caller, **kwargs):

    offer = kwargs.get("offer")
    item = kwargs.get("item")

    caller.db.gold += offer
    item.move_to(caller.location.db.storeroom, quiet = True)
    rtext = "you gain %i gold from the sale of %s!" % \
                       (offer, item.key)

    caller.msg(rtext)

def menunode_buy_home(caller):

    shopname = caller.location.key
    wares = caller.location.db.storeroom.contents
    text = ""

    #Wares includes everything in the storeroom including the door.  Dont sell the door

    wares = [ware for ware in wares if ware.key.lower() not in ("door", "storekey")]

    if wares:
        text += " Things for sale (choose 1-%i to inspect);"\
                " quit to exit:" %len(wares)
    else:
        text += "  There is nothing for sale; quit to exit"

    options = []

    for ware in wares:
        options.append({"desc": "%s (%s gold)" %
                           (ware.key, ware.db.value or 1),
                           "goto" : "menunode_inspect_and_buy"})

    return text, options


def menunode_inspect_and_buy(caller, raw_string):

    wares = caller.location.db.storeroom.contents
    wares = [ware for ware in wares if ware.key.lower() not in ("door", "storekey")]
    iware = int(raw_string) -1
    ware = wares[iware]
    value = ware.db.value or 1
    wealth = caller.db.gold or 0
    text = "You inspect %s:\n\n%s" % (ware.key, ware.db.desc)

    options = ({"desc": "Buy %s for %s gold" %\
                (ware.key, ware.db.value or 1),
                "exec": ("buy_ware_result", {"wealth" : wealth, "value" : value, "ware" : ware}),
                "goto": "menunode_shopfront"},
                {"desc": "Look for something else",
                "goto": "menunode_shopfront"})

    return text, options

def buy_ware_result(caller, **kwargs):

    wealth = kwargs.get("wealth")
    value = kwargs.get("value")
    ware = kwargs.get("ware")
    if wealth >= value:
        rtext = "you pay %i gold and purchase %s!" % \
                       (value, ware.key)
        caller.db.gold -= value
        ware.move_to(caller, quiet = True)
    else:
        rtext = "You cannot afford %i gold for %s!" % \
                (value, ware.key)
    caller.msg(rtext)

