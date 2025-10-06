from enum import Enum
from helper import Helper
import config
import nltk
from nltk.tokenize import wordpunct_tokenize
nltk.download("punkt")
from nltk.tokenize import sent_tokenize
from model.error_tag import ErrorTag

# Represents <Unit> in the paper https://doi.org/10.1007/s10579-024-09794-0
class Unit(Enum):

    NONE = 'None'
    GRAPHEME = 'Grapheme'
    AFFIX = 'Affix'
    LEMMA = 'Lemma'
    WORD = 'Word'
    MWE = 'Multi-word Expression' # not used
    PHRASE = 'Phrase'
    SENTENCE = 'Sentence'

    @staticmethod
    def mapUnit(err, line_list, overlap_flag, sentence):
        if err.errType == ErrorTag.DİJ.value:
            return Unit.NONE
        elif err.errType == ErrorTag.Dİ.value:
            return Unit.GRAPHEME
        elif err.errType in [ErrorTag.KI.value, ErrorTag.ST.value, ErrorTag.KEG.value]:
            return Unit.WORD
        elif err.errType in [ErrorTag.ÜDü.value, ErrorTag.ÜDa.value, ErrorTag.ÜzT.value]:
            return Unit.LEMMA
        elif err.errType in [ErrorTag.ÜU.value, ErrorTag.KH.value, ErrorTag.ÜzB.value, ErrorTag.DU.value, ErrorTag.SA.value,
                            ErrorTag.İY.value, ErrorTag.ÇA.value, ErrorTag.ZA.value, ErrorTag.KİP.value, ErrorTag.GÖ.value,
                            ErrorTag.ŞA.value, ErrorTag.ÇF.value, ErrorTag.SE.value, ErrorTag.KK.value, ErrorTag.GE.value,
                            ErrorTag.TÜ.value, ErrorTag.AB.value, ErrorTag.KBF.value]:
            return Unit.AFFIX
        elif err.errType == ErrorTag.NO.value:
            # extracting punctuation marks in original and corrected texts 
            corrPunct = Helper.extract_punctuation_marks_TR(err.corrText)
            incorrPunct = Helper.extract_punctuation_marks_TR(err.incorrText)

            # checking symmetric difference between original and corrected texts is checked
            # if there is an apostroph character in symmetric difference or corrected text is in abbreviation list of TDK, return WORD, else return SENTENCE
            if any(mark in list(set(corrPunct) ^ set(incorrPunct)) for mark in ["'", '´', '`']) or err.corrText.lower() in config.ABBREVIATIONS_TDK:
                return Unit.WORD
            else:
                return Unit.SENTENCE
        elif err.errType == ErrorTag.YA.value:
            if len(line_list) == 0:
                return Unit.NONE

            lemmas = []
            if overlap_flag:
                tokens = wordpunct_tokenize(err.corrText)

                for token in tokens:
                    multi_token_flag = False

                    for line in line_list:
                        cols = line.split("\t")
                        
                        # if the multi-token flag is on, then keep adding lines until the end index is reached
                        if multi_token_flag:
                            lemmas.append(cols[2]) # COL2 is LEMMA
                            multi_token_flag = False

                        if cols[1].lower() == token.lower():
                            if "-" in cols[0]:
                                multi_token_flag = True
                            else:
                                lemmas.append(cols[2]) # COL2 is LEMMA

            else:
                for line in line_list:
                    cols = line.split("\t")
                    lemmas.append(cols[2]) # COL2 is LEMMA
            
            if len(lemmas) == 0:
                return Unit.NONE
            # use the first one (spell errors are assumed to be annotated for a single token only)
            # if incorrect text starts with the lemma with phonologic event (stem), then the error occured in the AFFIX, else in the LEMMA
            if (err.incorrText.lower()).startswith(lemmas[0].lower()):
                return Unit.AFFIX
            else:
                return Unit.LEMMA
        elif err.errType == ErrorTag.BA.value:
            corrTxtLower = err.corrText.lower()
            # if no spacing exists in the corrected form and some affixes exist in the corrected form, return AFFIX
            # for all other cases including if any spacing exists in corrected form, return WORD
            if (" " not in corrTxtLower) and (corrTxtLower[-3:] in ["dır", "dir", "dur", "dür", "tır", "tir", "tur", "tür", "dan", "den", "tan", "ten"] or corrTxtLower[-2:] in ["de", "da", "te", "ta"]):
                return Unit.AFFIX
            else:
                return Unit.WORD
        elif err.errType == ErrorTag.BH.value:
            if len(line_list) == 0:
                return Unit.NONE

            if overlap_flag:
                tokens = wordpunct_tokenize(err.corrText)
                for token in tokens:
                    for line in line_list:
                        cols = line.split("\t")
                        if cols[1].lower() == token.lower() and cols[0] == "1":
                            return Unit.SENTENCE
            else:
                for line in line_list:
                    cols = line.split("\t")
                    if cols[0] == "1":
                        return Unit.SENTENCE
                
            #if (len(err.incorrText.split()) == len(err.corrText.split()) and len(err.incorrText.split()) > 1):
            if len(err.corrText.split()) > 1:
                return Unit.PHRASE
            else:
                return Unit.WORD
        elif err.errType == ErrorTag.ÜzY.value:
            if len(line_list) == 0:
                return Unit.NONE

            # consonant voicing errors are assumed to be annotated for a single token only
            tokens = wordpunct_tokenize(err.corrText)
            
            lemmas = []
            if overlap_flag:
                tokens = wordpunct_tokenize(err.corrText)

                for token in tokens:
                    multi_token_flag = False

                    for line in line_list:
                        cols = line.split("\t")
                        
                        # if the multi-token flag is on, then keep adding lines until the end index is reached
                        if multi_token_flag:
                            lemmas.append(cols[2]) # COL2 is LEMMA
                            multi_token_flag = False

                        if cols[1].lower() == token.lower():
                            if "-" in cols[0]:
                                multi_token_flag = True
                            else:
                                lemmas.append(cols[2]) # COL2 is LEMMA

            else:
                for line in line_list:
                    cols = line.split("\t")
                    lemmas.append(cols[2]) # COL2 is LEMMA

            if len(lemmas) == 0:
                return Unit.NONE

            if (err.incorrText[:len(lemmas[0])][-1] == "p" and err.corrText[:len(lemmas[0])][-1] == "b") and (err.incorrText[:len(lemmas[0])][-1] == "ç" and err.corrText[:len(lemmas[0])][-1] == "c") and (err.incorrText[:len(lemmas[0])][-1] == "t" and err.corrText[:len(lemmas[0])][-1] == "d") and (err.incorrText[:len(lemmas[0])][-1] == "k" and err.corrText[:len(lemmas[0])][-1] == "ğ"):
                return Unit.LEMMA
            else:
                return Unit.AFFIX
        elif err.errType == ErrorTag.SI.value:            
            if not overlap_flag:
                tokens_sentence = wordpunct_tokenize(sentence)
                tokens_corrText = wordpunct_tokenize(err.corrText)
                if len(tokens_sentence) == len(tokens_corrText):
                    return Unit.SENTENCE
            
            #if (len(err.incorrText.split()) == len(err.corrText.split()) and len(err.incorrText.split()) > 1):
            if len(err.corrText.split()) > 1:
                return Unit.PHRASE
            elif len(err.corrText.split()) == 1: 
                return Unit.AFFIX
            else:
                return Unit.NONE
        elif err.errType == ErrorTag.OL.value:
            tokens_erroredText = err.incorrText.split()
            if len(tokens_erroredText) > 1 and len(err.corrText.split()) == 1:
                return Unit.WORD
            return Unit.AFFIX
        elif err.errType == ErrorTag.SH.value:
            # SH errors may have empty err.corrText (because it is capable to take OMISSION value for its Phenomenon facet)
            if len(err.corrText.split()) == 0:
                if len(err.incorrText.split()) > 1:
                    return Unit.PHRASE
                else:
                    return Unit.WORD
            else:
                if len(err.corrText.split()) > 1:
                    return Unit.PHRASE
                else:
                    return Unit.WORD
        elif err.errType == ErrorTag.İB.value:
            # İB errors are assumed to be SENTENCE or PHRASE level only
            tokens_incorrText = wordpunct_tokenize(err.incorrText)
            sentence_list = sent_tokenize(err.rawText)
            for sent in sentence_list:
                tokens_sent = wordpunct_tokenize(sent)
                if tokens_sent == tokens_incorrText:
                    return Unit.SENTENCE
            if len(err.corrText.split()) > 1:
                return Unit.PHRASE
            return Unit.NONE
        elif err.errType == ErrorTag.AnB.value:
            # AnB errors have empty err.corrText
            tokens_incorrText = wordpunct_tokenize(err.incorrText)
            sentence_list = sent_tokenize(err.rawText)
            for sent in sentence_list:
                tokens_sent = wordpunct_tokenize(sent)
                if tokens_sent == tokens_incorrText:
                    return Unit.SENTENCE
            if len(err.incorrText.split()) > 1:
                return Unit.PHRASE
            return Unit.WORD
        elif err.errType == ErrorTag.ÜS.value:
            if len(line_list) == 0:
                return Unit.NONE

            lemma = ""
            token = wordpunct_tokenize(err.corrText)
            for line in line_list:
                cols = line.split("\t")
                if cols[1] == token:
                    lemma = cols[2]
                    break

            if (err.incorrText.split()[0].lower()).startswith(lemma.lower()):
                return Unit.AFFIX
            else:
                return Unit.WORD