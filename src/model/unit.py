from enum import Enum

class Unit(Enum):
    """ Represents <Unit> in the paper https://doi.org/10.1007/s10579-024-09794-0 """
    
    NONE = 0
    GRAPHEME = 1
    AFFIX = 2
    LEMMA = 3
    WORD = 4
    MWE = 5
    PHRASE = 6
    SENTENCE = 7

    @staticmethod
    def mapUnit(errType):
        mapping = {
        'HN': Unit.WORD, # Unit.__mapUnitForHN(incorrText.lower(), corrText.lower()),
        'BA': Unit.WORD, # Unit.__mapUnitForBA(incorrText.lower(), corrText.lower()),
        'Dİ': Unit.GRAPHEME,
        'BH': Unit.WORD, # Unit.__mapUnitForBH(incorrText, corrText, sentOrig),
        'KI': Unit.WORD,
        'YA': Unit.WORD # Unit.__mapUnitForYA(incorrText.lower(), corrText.lower())
        }

        return mapping.get(errType, Unit.NONE)