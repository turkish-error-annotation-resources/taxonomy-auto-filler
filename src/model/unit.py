from enum import Enum
from helper import Helper
import globals

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
    def mapUnit(errType, corrTxt, incorrTxt):
        match errType:
            case 'HN':
                """
                punct. marks in original and corrected texts are extracted
                symmetric difference between original and corrected texts is checked
                if there is an apostroph character in symmetric difference OR corrected text is in abbreviation list of TDK -> WORD
                otherwise -> SENTENCE
                """

                corrPunct = Helper.extract_punctuation_marks_TR(corrTxt)
                incorrPunct = Helper.extract_punctuation_marks_TR(incorrTxt)

                if any(mark in list(set(corrPunct) ^ set(incorrPunct)) for mark in ["'", '´', '`']) or corrTxt.lower() in globals.abbr_list_TR:
                    return Unit.WORD
                else:
                    return Unit.SENTENCE
            case 'BA':
                """
                if any spacing exists in corrected form -> WORD
                if no spacing exists in the corrected form AND some affixes exist in the corrected form -> AFFIX
                for all other cases -> WORD
                """

                corrTxt = corrTxt.lower()
                if (" " not in corrTxt) and (corrTxt[-3:] in ["dır", "dir", "dur", "dür", "tır", "tir", "tur", "tür", "dan", "den", "tan", "ten"] or corrTxt[-2:] in ["de", "da", "te", "ta"]):
                    return Unit.AFFIX
                else:
                    return Unit.WORD
            case 'Dİ':
                return Unit.NONE
            case 'BH':
                return Unit.NONE
            case 'KI':
                return Unit.NONE
            case 'YA':
                return Unit.NONE
        """
        mapping = {
            'HN': Unit.WORD, # Unit.__mapUnitForHN(incorrText.lower(), corrText.lower()),
            'BA': Unit.WORD, # Unit.__mapUnitForBA(incorrText.lower(), corrText.lower()),
            'Dİ': Unit.GRAPHEME,
            'BH': Unit.WORD, # Unit.__mapUnitForBH(incorrText, corrText, sentOrig),
            'KI': Unit.WORD,
            'YA': Unit.WORD # Unit.__mapUnitForYA(incorrText.lower(), corrText.lower())
        }

        return mapping.get(errType, Unit.NONE)
        """