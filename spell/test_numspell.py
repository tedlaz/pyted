"""Testing Module"""
import unittest
import numspell as ns


class TestNumspell(unittest.TestCase):
    """Main test"""
    def test_01(self):
        self.assertEqual(ns.num2text(1), 'ένα')

    def test_02(self):
        self.assertEqual(ns.num2text(11), 'έντεκα')

    def test_03(self):
        self.assertEqual(ns.num2text(65), 'εξήντα πέντε')

    def test_04(self):
        self.assertEqual(ns.num2text(99), 'ενενήντα εννέα')

    def test_05(self):
        self.assertEqual(ns.num2text(112), 'εκατόν δώδεκα')

    def test_06(self):
        self.assertEqual(ns.num2text(2112), 'δύο χιλιάδες εκατόν δώδεκα')

    def test_07(self):
        self.assertEqual(ns.num2text(9999), 'εννέα χιλιάδες εννιακόσια ενενήντα εννέα')

    def test_08(self):
        self.assertEqual(ns.num2text(1012), 'χίλια δώδεκα')

    def test_09(self):
        self.assertEqual(ns.num2text(10012), 'δέκα χιλιάδες δώδεκα')

    def test_10(self):
        self.assertEqual(ns.num2text(900000), 'εννιακόσιες χιλιάδες')

    def test_11(self):
        self.assertEqual(ns.num2text(912123), 'εννιακόσιες δώδεκα χιλιάδες εκατόν είκοσι τρία')


if __name__ == '__main__':
    print(ns.num2text(0))
    print(ns.num2text(1))
    print(ns.num2text(100))
    print(ns.num2text(1000))
    print(ns.num2text(10000))
    print(ns.num2text(101000))
