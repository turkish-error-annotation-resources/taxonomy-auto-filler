from enum import Enum
from helper import Helper

class LexFeat(Enum):
    """ Represents <LexicalFeature> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    # not applicable for Turkish
    POSS = 'Possessive' # ???
    OTHER_ABBR = 'Abbreviation' # ???
    OTHER_TYPO = 'Typo' # ???
    OTHER_FOREIGN = 'Foreign'
    OTHER_EXTPOS = 'ExternalPOS'
    # applicable for Turkish
    PRONTYPE = 'PronType'
    NUMTYPE = 'Numtype'
    REFLEX = 'Reflex'
    
    @staticmethod
    def mapLexFeat(err):
        resLexFeat = []

        if err.errType == 'KI':
            resLexFeat.append(LexFeat.OTHER_ABBR)
        elif err.errType == 'YA':
            resLexFeat.append(LexFeat.OTHER_TYPO)

        return resLexFeat