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
                """
                set operations are used heuristically, it can be improved by different approaches (using character frequency dictionary, etc.)
                """

                diff_list = list(set(corrTxt) - set(incorrTxt))
                diff_list2 = list(set(incorrTxt) - set(corrTxt))

                add = 0
                omm = 0
                els = 0

                for char in diff_list:
                    if char in ["İ", "Ü", "Ö", "Ğ", "Ş", "Ç", "i", "ü", "ö", "ğ", "ş", "ç", "j", "î", "Î", "â", "Â"]:
                        omm += 1
                    elif char in ["I", "U", "O", "G", "S", "C", "ı", "u", "o", "g", "s", "c", "J", "a", "A"]:
                        add += 1
                    else:
                        els += 1

                for char in diff_list2:
                    if char in ["İ", "Ü", "Ö", "Ğ", "Ş", "Ç", "i", "ü", "ö", "ğ", "ş", "ç", "j", "î", "Î", "â", "Â"]:
                        add += 1
                    elif char in ["I", "U", "O", "G", "S", "C", "ı", "u", "o", "g", "s", "c", "J", "a", "A"]:
                        omm += 1
                    else:
                        els += 1

                if add > 0 and omm > 0:
                    return Phenomenon.MISUSE
                elif add > 0:
                    return Phenomenon.ADDITION
                elif omm > 0:
                    return Phenomenon.OMISSION
                else:
                    return Phenomenon.NONE
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