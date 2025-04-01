from enum import Enum

class POS(Enum):
    """ Represents <Part-of-speech> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 0
    ADJ = 1 #
    ADP = 2 #
    ADV = 3 #
    AUX = 4 #
    CCONJ = 5 #
    DET = 6 #
    INTJ = 7 #
    NOUN = 8 #
    NUM = 9 #
    PART = 10 #
    PRON = 11 #
    PROPN = 12 #
    PUNCT = 13 #
    SCONJ = 14 #
    SYM = 15 #
    VERB = 16 #
    X = 17 #

    @staticmethod
    def mapPOS(errType):
        mapping = {
        'HN': POS.PUNCT,
        'BA': POS.NONE, # POS.__mapPOS(incorrText, corrText, corrSent),
        'Dİ': POS.NONE, # POS.__mapPOS(incorrText, corrText, corrSent),
        'BH': POS.NONE, # POS.__mapPOS(incorrText, corrText, corrSent),
        'KI': POS.NONE, # POS.__mapPOS(incorrText, corrText, corrSent),
        'YA': POS.NONE # POS.__mapPOS(incorrText, corrText, corrSent)
        }

        return mapping.get(errType, POS.NONE)