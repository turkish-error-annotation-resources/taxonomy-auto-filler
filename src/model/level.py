from enum import Enum

class Level(Enum):
    """ Represents <Linguistic Level> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 0
    PHONOLOGY = 1
    ORTHOGRAPHY = 2
    GRAMMAR = 3
    SEMANTICS = 4
    PRAGMATICS = 5
    DISCOURSE = 6
    SOCIOLINGUISTIC = 7

    @staticmethod
    def mapLevel(errType):
        mapping = {
        'HN': Level.ORTHOGRAPHY,
        'BA': Level.ORTHOGRAPHY,
        'Dİ': Level.ORTHOGRAPHY,
        'BH': Level.ORTHOGRAPHY,
        'KI': Level.ORTHOGRAPHY,
        'YA': Level.ORTHOGRAPHY
        }
        
        return mapping.get(errType, Level.NONE)