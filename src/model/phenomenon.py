from enum import Enum

class Phenomenon(Enum):
    """ Represents <Phenomenon> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 0
    OMISSION = 1 # the absence of an item that must appear in a well-formed utterance
    ADDITION = 2 # the presence of an item that should not appear in a well-formed utterance
    MISUSE = 3 # the use of the wrong form of the morpheme or structure
    MISORDERING = 4 # the incorrect placement of a morpheme or a group of morphemes in an utterance
    UNTRANSLATED = 5
    AMBIGUITY = 6

    @staticmethod
    def mapPhenomenon(errType):
        mapping = {
        'HN': Phenomenon.MISUSE, #Phenomenon.__mapPhenomenonForHN(incorrText.lower(), corrText.lower()),
        'BA': Phenomenon.MISUSE,
        'Dİ': Phenomenon.MISUSE, #Phenomenon.__mapPhenomenonForDI(incorrText, corrText),
        'BH': Phenomenon.MISUSE,
        'KI': Phenomenon.MISUSE,
        'YA': Phenomenon.MISUSE #Phenomenon.__mapPhenomenonForYA(incorrText.strip(), corrText.strip())
        }

        return mapping.get(errType, Phenomenon.NONE)