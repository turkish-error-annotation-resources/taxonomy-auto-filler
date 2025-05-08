from enum import Enum
from helper import Helper
import globals

class Unit(Enum):
    """ Represents <Unit> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    GRAPHEME = 'Grapheme'
    AFFIX = 'Affix'
    LEMMA = 'Lemma'
    WORD = 'Word'
    MWE = 'Multi-word Expression'
    PHRASE = 'Phrase'
    SENTENCE = 'Sentence'

    def __str__(self):
        return self.value

    @staticmethod
    def mapUnit(err):
        match err.errType:
            # PUNCTUATION
            case 'HN': 
                """
                punctuation marks in original and corrected texts are extracted
                symmetric difference between original and corrected texts is checked
                if there is an apostroph character in symmetric difference or corrected text is in abbreviation list of TDK, return WORD, else return SENTENCE
                """
                corrPunct = Helper.extract_punctuation_marks_TR(err.corrText)
                incorrPunct = Helper.extract_punctuation_marks_TR(err.incorrText)

                if any(mark in list(set(corrPunct) ^ set(incorrPunct)) for mark in ["'", '´', '`']) or err.corrText.lower() in globals.abbr_list_TR:
                    return Unit.WORD
                else:
                    return Unit.SENTENCE
            # SPACING
            case 'BA':
                """
                if no spacing exists in the corrected form and some affixes exist in the corrected form, return AFFIX
                for all other cases including if any spacing exists in corrected form, return WORD
                # todo: affix list may be extended
                """
                corrTxtLower = err.corrText.lower()
                if (" " not in corrTxtLower) and (corrTxtLower[-3:] in ["dır", "dir", "dur", "dür", "tır", "tir", "tur", "tür", "dan", "den", "tan", "ten"] or corrTxtLower[-2:] in ["de", "da", "te", "ta"]):
                    return Unit.AFFIX
                else:
                    return Unit.WORD
            # DIACRITICS
            case 'Dİ':
                """
                direct mapping
                """
                return Unit.GRAPHEME
            # CAPITALIZATION
            case 'BH':
                """
                if the error occurs at the begining of the sentence, return SENTENCE
                if there are more than one token in the original and corrected texts, and their lengths are equal, return PHRASE, else return WORD
                """
                # extract tokens from the original sentence
                tokens = err.sentOrig.split()

                if tokens[0] == err.incorrText:
                    return Unit.SENTENCE
                elif (len(err.incorrText.split()) == len(err.corrText.split()) and len(err.incorrText.split()) > 1):
                    return Unit.PHRASE
                else:
                    return Unit.WORD
            # ABBREVIATION
            case 'KI':
                """
                direct mapping
                """
                return Unit.WORD
            # SPELLING
            case 'YA':
                """
                spell errors are assumed to be annotated for a single token only
                if corrected text has more than one token, return the first result of the detection
                if corrected text cannot be analyzed, return NONE
                if incorrect text starts with the first element of the surfaceForm (which is lemma with phonological event), return AFFIX, else return LEMMA
                """
                corrTxtLower = err.corrText.lower()
                incorrTxtLower = err.incorrText.lower()

                # we're sure it returns a list with 1 element or 0 (if it cannot be analyzed)
                analysisList = Helper.get_morpholocial_analysis(err)

                for analysis in analysisList:
                   # be sure it can be analyzed
                    if str(analysis.getPos()) != "Unknown":
                        morphemeSurfaceList = [m.surface for m in analysis.getMorphemeDataList()] # e.g. ['ağac', '', 'ın']
                        lemmaWithPhonologicEvent = str(morphemeSurfaceList[0]) # stem
                        
                        # if incorrect text starts with the lemma with phonologic event (stem), then the error occured in the AFFIX, else in the LEMMA
                        if incorrTxtLower.startswith(lemmaWithPhonologicEvent):
                            return Unit.AFFIX
                        else:
                            return Unit.LEMMA
                return Unit.NONE
            # CONSONANT VOICING
            case 'ÜzY':
                """
                consonant voicing errors are assumed to be annotated for a single token only
                if corrected text has more than one token, return the first result of the detection
                if corrected text cannot be analyzed, return NONE
                if the last character of the lemma with phonologic event is transformed from "p, ç, t, k" to "b, c, d, ğ", return LEMMA, else return AFFIX
                """
                corrTxtLower = err.corrText.lower()
                incorrTxtLower = err.incorrText.lower()
                
                # we're sure it returns a list with 1 element or 0 (if it cannot be analyzed)
                analysisList = Helper.get_morpholocial_analysis(err)

                for analysis in analysisList:
                    # be sure it can be analyzed
                    if str(analysis.getPos()) != "Unknown":
                        morphemeSurfaceList = [m.surface for m in analysis.getMorphemeDataList()] # e.g. ['ağac', '', 'ın']
                        lemmaWithPhonologicEvent = str(morphemeSurfaceList[0]) # stem

                        # if consonant voicing is observed in lemmaWithPhonologicEvent (stem)
                        if (lemmaWithPhonologicEvent[-1] == "b" and incorrTxtLower[:len(lemmaWithPhonologicEvent)][-1] == "p") or (lemmaWithPhonologicEvent[-1] == "c" and incorrTxtLower[:len(lemmaWithPhonologicEvent)][-1] == "ç") or (lemmaWithPhonologicEvent[-1] == "d" and incorrTxtLower[:len(lemmaWithPhonologicEvent)][-1] == "t") or (lemmaWithPhonologicEvent[-1] == "ğ" and incorrTxtLower[:len(lemmaWithPhonologicEvent)][-1] == "k"):
                            return Unit.LEMMA
                        else:
                            return Unit.AFFIX
                return Unit.NONE
            # VOWEL HARMONY
            case 'ÜU':
                """
                direct mapping
                """
                return Unit.AFFIX
            # VOWEL DROPPING
            case 'ÜD':
                """
                direct mapping
                """
                return Unit.LEMMA
            # BUFFER LETTERS
            case 'KH':
                """
                direct mapping
                """
                return Unit.AFFIX
            # CONSONANT ASSIMILATION
            case 'ÜzB':
                """
                direct mapping
                """
                return Unit.AFFIX
            # VOWEL NARROWING
            case 'ÜDa':
                """
                direct mapping
                """
                return Unit.LEMMA
            # CONSONANT DOUBLING
            case 'ÜzT':
                """
                direct mapping
                """
                return Unit.LEMMA