from enum import Enum
from model.error_tag import ErrorTag

# Represents <Linguistic Level> in the paper https://doi.org/10.1007/s10579-024-09794-0
class Level(Enum):

    NONE = 'None'
    MORPHOPHONOLOGY = 'Morphophonology'
    ORTHOGRAPHY = 'Orthograpy'
    GRAMMAR = 'Grammar'
    SEMANTICS = 'Semantics'
    PRAGMATICS = 'Pragmatics'
    DISCOURSE = 'Discourse' # not used
    SOCIOLINGUISTIC = 'Sociolinguistic' # not used

    @staticmethod
    def mapLevel(err):
        if err.errType in [ErrorTag.NO.value, ErrorTag.YA.value, ErrorTag.BA.value, ErrorTag.BH.value, ErrorTag.Dİ.value, ErrorTag.KI.value]:
            return Level.ORTHOGRAPHY
        elif err.errType in [ErrorTag.ÜzY.value, ErrorTag.ÜDü.value, ErrorTag.ÜU.value, ErrorTag.KH.value, ErrorTag.ÜzB.value, ErrorTag.ÜDa.value, ErrorTag.ÜzT.value]:
            return Level.MORPHOPHONOLOGY
        elif err.errType in [ErrorTag.SI.value, ErrorTag.DU.value, ErrorTag.SA.value, ErrorTag.İY.value, ErrorTag.ÇA.value, ErrorTag.ZA.value, ErrorTag.KİP.value,
                            ErrorTag.GÖ.value, ErrorTag.OL.value, ErrorTag.ŞA.value, ErrorTag.ÇF.value, ErrorTag.SE.value, ErrorTag.KK.value, ErrorTag.GE.value,
                            ErrorTag.ST.value, ErrorTag.TÜ.value, ErrorTag.AB.value, ErrorTag.KEG.value, ErrorTag.KBF.value]:
            return Level.GRAMMAR
        elif err.errType in [ErrorTag.AnB.value]:
            return Level.SEMANTICS
        elif err.errType in [ErrorTag.ÜS.value]:
            return Level.PRAGMATICS
        else:
            return Level.NONE
