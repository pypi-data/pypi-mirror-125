"""
Translator module allows to change natural language to mathematical notation.
"""
from verbcalc.core.symbols import Symbols

DEFAULT_SYMBOLS = Symbols()


def _translate_additions(sentence: str, symbols: Symbols) -> str:
    result = ''
    buffer = sentence.split()

    for word in buffer:
        if word in symbols.additions:
            new_word = ' + '
        else:
            new_word = word

        result += new_word

    return result


def translate(sentence: str, symbols: Symbols = DEFAULT_SYMBOLS) -> str:
    """
      Translates maths related words into their symbols.

      Args:
          sentence: Sentence to be converted.
          symbols: Instance of symbols to match the words from.

      Returns:
          Converted sentence.
    """
    return _translate_additions(sentence.lower(), symbols)
