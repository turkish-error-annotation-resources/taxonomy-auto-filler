from enum import Enum
from helper import Helper

class POS(Enum):
    """ Represents <Part-of-speech> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'                       # not used
    ADJ = 'Adjactive'                   # +
    ADP = 'Adposition'                  # + determined by using zemberek's primaryPOS "PostPositive"
    ADV = 'Adverb'                      # +
    AUX = 'Auxiliary'                   # + determined by using zemberek's primaryPOS "Question" (a heuristic that counts the same aux in the sentence, if == 2 then highly possible to be sconj!) todo: what about "ol" and "bulun" ???
    CCONJ = 'Coordinating Conjunction'  # + (further filtered by using Conjunction)
    DET = 'Determiner'                  # +
    INTJ = 'Interjection'               # +
    NOUN = 'Noun'                       # +
    NUM = 'Numeral'                     # +
    PART = 'Particle'                   # - use it for the word "değil" when used to negate a non-predicate word, if "değil" modifies a predicate, it is marked as VERB since it functions as a copula and carries other verbal inflections as well
    PRON = 'Pronoun'                    # +
    PROPN = 'Proper Noun'               # +
    PUNCT = 'Punctuation'               # +
    SCONJ = 'Subordinating Conjunction' # + (further filtered by using Conjunction)
    SYM = 'Symbol'                      # + (determined by using secondaryPOS -> Mention, HashTag, Emoticon, RomanNumeral)
    VERB = 'Verb'                       # +
    X = 'Other'                         # + (Unknown)
    CONJ = 'Conjunction'                # extended POS (will be used in case of not determining it as SCNOJ or CCONJ)

    def __str__(self):
        return self.value
    
    # CCONJ: Coordinating Conjunctions
    __cconj_list = {"ve", "ama", "fakat", "ancak", "veya", "ya da", "ne", "hem", "ile", "lakin", "yahut", "ya", "de", "da"}
    # SCONJ: Subordinating Conjunctions
    __sconj_list = {"çünkü", "ki", "diye", "madem", "eğer", "sanki", "nasıl", "ise", "yeter ki", "gibi", "için"}

    @staticmethod
    def mapPOS(err):
        match err.errType:
            # PUNCTUATION
            case 'HN':
                return [POS.PUNCT]
            case 'ES': # todo: will be deleted
                return [POS.NONE]
            case 'KS': # todo: will be deleted
                return [POS.NONE]
            #case 'SI': # todo: will be added to LS at the end
                return [POS.NONE]
            case 'SE':
                return [POS.NONE]
            #  OTHERS
            case _:
                posList = Helper.get_POS(err.sentCorr, err.corrText)
                
                res = []
                for posRecord in posList:
                    if posRecord["posSecondary"] in ["Mention", "HashTag", "Emoticon", "RomanNumeral"]:
                        res.append(POS.SYM)
                    elif posRecord["posPrimary"] == 'Adjective':
                        res.append(POS.ADJ)
                    elif posRecord["posPrimary"] == 'Adverb':
                        res.append(POS.ADV)
                    elif posRecord["posPrimary"] == 'Question':
                        count = 0
                        for e in posList:
                            if e["surfaceForm"].strip().lower() == posRecord["surfaceForm"].strip().lower():
                                count += 1
                        # if it contains the same question particle twice in the sentence then it is probably (highly) sconj, else it is aux
                        if count == 2:
                            res.append(POS.SCONJ) 
                        else:
                            res.append(POS.AUX)
                    elif posRecord["posPrimary"] == 'Conjunction':
                        if posRecord["surfaceForm"].strip().lower() in POS.__cconj_list:
                            res.append(POS.CCONJ)
                        elif posRecord["surfaceForm"].strip().lower() in POS.__sconj_list:
                            res.append(POS.SCONJ)
                        else:
                            res.append(POS.CONJ)
                    elif posRecord["posPrimary"] == 'Determiner':
                        res.append(POS.DET)
                    elif posRecord["posPrimary"] == 'Noun' and posRecord["posSecondary"] == 'ProperNoun':
                        res.append(POS.PROPN)
                    elif posRecord["posPrimary"] == 'Noun':
                        res.append(POS.NOUN)
                    elif posRecord["posPrimary"] == 'Interjection':
                        res.append(POS.INTJ)
                    elif posRecord["posPrimary"] == 'Numeral':
                        res.append(POS.NUM)
                    elif posRecord["posPrimary"] == 'Verb':
                        res.append(POS.VERB)
                    elif posRecord["posPrimary"] == 'Pronoun':
                        res.append(POS.PRON)
                    elif posRecord["posPrimary"] == 'Punctuation': 
                        res.append(POS.PUNCT)
                    elif posRecord["posPrimary"] == 'PostPositive':
                        res.append(POS.ADP)
                    else: 
                        res.append(POS.X)
        
                return res