from evennia.utils.test_resources import EvenniaTest
from .spells import Spell


class TestSpell(EvenniaTest):

    def setUp(self):
        super().setUp()
        self.spell = Spell(self.char1, 'Firebolt', None)
        self.spell.mana_cost = 25
        self.char1.db.mana = 100

    def test_has_enough_mana(self):
        actual_return = self.spell.has_enough_mana()
        expected_return = True
        self.assertEqual(expected_return, actual_return)
