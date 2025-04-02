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
    def mapUnit(errType, corrTxt, incorrTxt, sentOrig):
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
                return Unit.GRAPHEME
            case 'BH':
                """
                if the begining of the sentence -> SENTENCE
                if more than one token for the original and corrected texts and their lengths are equal -> PHRASE
                owtherwise -> WORD
                """

                words = sentOrig.split()
                if words[0] == incorrTxt:
                    return Unit.SENTENCE
                elif (len(incorrTxt.split()) == len(corrTxt.split()) and len(incorrTxt.split()) > 1):
                    return Unit.PHRASE
                else:
                    return Unit.WORD
            case 'KI':
                return Unit.WORD
            case 'YA':
                """
                spell errors are assumed to be annotated for a single token only
                if no lemma is found -> WORD
                if original text starts with the lemma of corrected form, then the error is occured in the affix part
                # todo: the last character of lemma will not be taken into consideration (maybe lemma[0][:-1] ??)
                """

                if len(corrTxt.split()) == 1:
                    lemma = Helper.get_lemmas(corrTxt)
                    lemma = str(lemma)

                    if lemma == "":
                        return Unit.WORD
                    else:
                        if incorrTxt.startswith(lemma):
                            return Unit.AFFIX
                        # doğru ve yanlış token'da lemma uzunluğu kadar karakteri çıkarıp kalan bölüm eşit ise, o zaman hata köktedir (böyle de olabilir?)
                        #elif corrTxt[len(lemma[0]):] == incorrTxt[len(lemma[0]):]: 
                        #    return Unit.LEMMA
                        else:
                            return Unit.LEMMA