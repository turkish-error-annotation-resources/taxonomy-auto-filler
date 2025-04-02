from enum import Enum
from helper import Helper

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
    def mapPhenomenon(errType, corrTxt, incorrTxt):
        match errType:
            case 'HN':
                """
                heuristical approach:  using th change in the number of punctiation marks
                if lengths of pnct. marks lists are equal, then there are two options: 
                    1- at least one element which is different -> MISUSE
                    2- no different element -> MISORDERING
                if there are more punct. marks in corrected form than in the original form -> OMISSION
                if there are less punct. marks in corrected form than in the original form -> ADDITION
                """

                corrPunct = Helper.extract_punctuation_marks_TR(corrTxt) # list of all punct. marks in the corrected text
                incorrPunct = Helper.extract_punctuation_marks_TR(incorrTxt) # list of all punct. marks in the original text
                
                if len(corrPunct) == len(incorrPunct):
                    if len(set(corrPunct) - set(incorrPunct)) > 0:
                        return Phenomenon.MISUSE
                    else:
                        return Phenomenon.MISORDERING
                elif len(corrPunct) > len(incorrPunct):
                    return Phenomenon.OMISSION
                elif len(corrPunct) < len(incorrPunct):
                    return Phenomenon.ADDITION
                else:
                    return Phenomenon.NONE
            case 'BA':
                return Phenomenon.MISUSE
            case 'Dİ':
                return Phenomenon.MISUSE
            case 'BH':
                return Phenomenon.MISUSE
            case 'KI':
                return Phenomenon.MISUSE
            case 'YA':
                return Phenomenon.MISUSE

        """
        mapping = {
        'HN': Phenomenon.MISUSE, #Phenomenon.__mapPhenomenonForHN(incorrText.lower(), corrText.lower()),
        'BA': Phenomenon.MISUSE,
        'Dİ': Phenomenon.MISUSE, #Phenomenon.__mapPhenomenonForDI(incorrText, corrText),
        'BH': Phenomenon.MISUSE,
        'KI': Phenomenon.MISUSE,
        'YA': Phenomenon.MISUSE #Phenomenon.__mapPhenomenonForYA(incorrText.strip(), corrText.strip())
        }"
        """

        #return mapping.get(errType, Phenomenon.NONE)