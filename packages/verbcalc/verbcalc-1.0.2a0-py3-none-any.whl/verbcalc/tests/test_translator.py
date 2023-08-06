"""
Tests translator module.
"""
import unittest

import verbcalc


class TestTranslator(unittest.TestCase):
    """
    Tests how translator works.
    """

    def setUp(self):
        self._custom_symbols = verbcalc.Symbols()
        self._custom_symbols.additions = ['foo', 'bar']
        self._expected = ['2 + 2', '2 + 2']

    def test_addition(self):
        values = [verbcalc.translate('2 plus 2'),
                  verbcalc.translate('2 Plus 2')]
        self.assertListEqual(self._expected, values)

    def test_translation_with_custom_symbols(self):
        values = [verbcalc.translate
                  ('2 foo 2', symbols=self._custom_symbols), verbcalc.translate
                  ('2 bar 2', symbols=self._custom_symbols)]
        self.assertListEqual(self._expected, values)


if __name__ == '__main__':
    unittest.main()
