from evennia.utils.test_resources import EvenniaTest, EvenniaCommandTestMixin
from .rooms import EnemyRoom
from evennia.objects.objects import ExitCommand
from evennia.commands.default.general import CmdLook
from evennia.utils.create import create_object


class TestEnemyRoom(EvenniaTest, EvenniaCommandTestMixin):

    def setUp(self):
        super().setUp()
        self.enemyroom = create_object(EnemyRoom,
                                       key="Room3",
                                       location=None)
        create_object(self.exit_typeclass, key="getout", location=self.room1, destination=self.enemyroom)

    def test_at_object_receive(self):
        # self.call(CmdLook(), '', msg="room")
        self.call(ExitCommand(), "getout", caller=self.char1, msg=None)
        self.call(CmdLook(), '', msg="Room")
