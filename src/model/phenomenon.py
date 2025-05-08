from enum import Enum
from helper import Helper
from collections import Counter

class Phenomenon(Enum):
    """ Represents <Phenomenon> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    OMISSION = 'Omission' # the absence of an item that must appear in a well-formed utterance
    ADDITION = 'Additiono' # the presence of an item that should not appear in a well-formed utterance
    MISUSE = 'Misuse' # the use of the wrong form of the morpheme or structure
    MISORDERING = 'Misordering' # the incorrect placement of a morpheme or a group of morphemes in an utterance
    UNTRANSLATED = 'Untranslated' # NOT USED
    AMBIGUITY = 'Ambiguity' # NOT USED

    def __str__(self):
        return self.value

    @staticmethod
    def mapPhenomenon(err): 
        match err.errType:
            # PUNCTUATION
            case 'HN':
                """
                heuristical approach:  using th change in the number of punctiation marks
                if lengths of pnct. marks lists are equal, then there are two options: 
                    1- at least one element which is different -> MISUSE
                    2- no different element -> MISORDERING
                if there are more punct. marks in corrected form than in the original form -> OMISSION
                if there are less punct. marks in corrected form than in the original form -> ADDITION
                """

                corrPunct = Helper.extract_punctuation_marks_TR(err.corrText) # list of all punct. marks in the corrected text
                incorrPunct = Helper.extract_punctuation_marks_TR(err.incorrText) # list of all punct. marks in the original text
                
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
            # SPACING
            case 'BA':
                return Phenomenon.MISUSE
            # DIACRITICS
            case 'Dİ':
                """
                set operations are used heuristically, it can be improved by different approaches (using character frequency dictionary, etc.)
                """

                diff_list = list(set(err.corrText) - set(err.incorrText))
                diff_list2 = list(set(err.incorrText) - set(err.corrText))

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
            # CAPITALIZATION
            case 'BH':
                return Phenomenon.MISUSE
            # ABBREVIATION
            case 'KI':
                return Phenomenon.MISUSE
            # SPELLING
            case 'YA':
                """
                if frequency of each character for both texts are equal -> MISORDERING
                if length of the original text is greater than the corrected text -> ADDITION
                if length of the original text is smaller than the corrected text -> OMISSION
                otherwise -> MISUSE
                """

                if (dict(Counter(err.incorrText)) == dict(Counter(err.corrText))):
                    return Phenomenon.MISORDERING
                elif len(err.incorrText) > len(err.corrText):
                    return Phenomenon.ADDITION
                elif len(err.incorrText) < len(err.corrText):
                    return Phenomenon.OMISSION
                else:
                    return Phenomenon.MISUSE
            # CONSONANT VOICING
            case 'ÜzY':
                """
                direct mapping
                """
                return Phenomenon.MISUSE
            # VOWEL HARMONY
            case 'ÜU':
                """
                direct mapping
                """
                return Phenomenon.MISUSE
            # VOWEL DROPPING
            case 'ÜD':
                """
                direct mapping
                """
                return Phenomenon.MISUSE
            # BUFFER LETTERS
            case 'KH':
                """
                assumption: incorrect text involves only KH error
                checks morphemes whether they start with "y" and "n" (buffer letters)
                if it is detected, compare it with the incorrect text
                """
                analysisList = Helper.get_morpholocial_analysis(err)
                for analysis in analysisList:
                    # be sure it can be analyzed
                    if str(analysis.getPos()) != "Unknown":
                        
                        morphemeSurfaceList = [m.surface for m in analysis.getMorphemeDataList()] # e.g. ['ağac', '', 'ın']
                        
                        index = 0
                        for idx, morpheme in enumerate(morphemeSurfaceList):
                            morpheme = str(morpheme)
                            index += len(morpheme)
                            if idx != 0 and (morpheme.startswith('y') or morpheme.startswith('n')):
                                if (err.incorrText == err.corrText[:(index - len(morpheme))] + err.corrText[(index - len(morpheme) + 1):]):
                                    return Phenomenon.OMISSION
                                
                                if len(err.incorrText) == len(err.corrText) and len(err.incorrText) > (index - len(morpheme)) and err.incorrText[index - len(morpheme)] != err.corrText[index - len(morpheme)]:
                                    return Phenomenon.MISUSE
                        
                        if len(err.incorrText) > len(err.corrText):
                            return Phenomenon.ADDITION
                        return Phenomenon.NONE
                return Phenomenon.NONE
            # CONSONANT ASSIMILATION
            case 'ÜzB':
                """
                direct mapping
                """
                return Phenomenon.MISUSE
            # VOWEL NARROWING
            case 'ÜDa':
                """
                direct mapping
                """
                return Phenomenon.MISUSE
            # CONSONANT DOUBLING
            case 'ÜzT':
                """
                direct mapping
                """
                return Phenomenon.MISUSE