from enum import Enum
from helper import Helper

class LexFeat(Enum):
    """ Represents <LexicalFeature> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    # not applicable for Turkish
    POSS = 'Possessive' # this feature is detected as inflectional feature in Turkish (expanded feature!)
    OTHER_ABBR = 'Abbreviation' # mapped to "KI" directly
    OTHER_TYPO = 'Typo' # mapped to "YA" directly
    OTHER_FOREIGN = 'Foreign'
    OTHER_EXTPOS = 'ExternalPOS'
    # applicable for Turkish
    PRONTYPE = 'PronType'
    NUMTYPE = 'NumType'
    REFLEX = 'Reflex'

    def __str__(self):
        return self.value

    #todo: is enum type necesssary?
    
    __pronList = ["ben", "sen", "biz", "siz", "benim", "senin", "bizim", "sizin", "benimki", "seninki", "bizimki", "sizinki"]

    __interrogativePronounList = [
        # "kim" kökenli
        "kim", "kimi", "kime", "kimde", "kimden", "kimin", "kiminki",

        # "ne" kökenli
        "ne", "neyi", "neye", "nede", "neden", "neyden", "neyin", "nenin", "neninki", "neyinki",

        # "kaç" kökenli
        "kaç", "kaçı", "kaça", "kaçta", "kaçtan",
        "kaçıncı", "kaçının", "kaçıncısı",

        # "hangi" kökenli
        "hangi", "hangisi", "hangisinin", "hangisine", "hangisinde",
        "hangisinden", "hangisini", "hangiler", "hangileri", "hangilerinin"
    ]

    __demonstrativePronounList = [
        # Singular
        "bu",       # this
        "şu",       # that (nearby)
        "o",        # that (far away)

        # Plural
        "bunlar",   # these
        "şunlar",   # those (nearby)
        "onlar",    # those (far away)

        # "-ki" forms (used for possession or specification)
        "bununki",
        "şununki",
        "onunki",
        "bunkiler",
        "şunkiler",
        "onunkiler",

        "bundaki",
        "şundaki",
        "ondaki",
        "bund   akiler",
        "şundakiler",
        "ondakiler"
    ]

    __indefinitePronounList = [
        "biri",           # someone
        "birisi",         # someone
        "birkaç",         # a few
        "birkaçı",        # a few of them
        "birşey",         # something (non-standard spelling)
        "herkes",         # everyone
        "herkesi",        # everyone (accusative)
        "herkese",        # to everyone
        "herkesten",      # from everyone
        "herkesin",       # everyone's
        "herşey",         # everything (non-standard spelling)
        "kimse",          # anyone / no one (depends on polarity)
        "bazı",           # some (used adjectivally but can be pronominal)
        "bazıları",       # some of them
        "bazısını",       # some (accusative)
        "birileri",       # some people
        "birilerini",     # some people (accusative)
        "birilerine",     # to some people
        "çoğu",           # most (of)
        "çoğunu",         # most of it (accusative)
        "azı",            # a little (of)
        "azını",          # a little of it (accusative)
        "diğeri",         # the other one
        "diğerleri",      # the others
        "hepsi",          # all
        "kimi",           # some (not to be confused with question word “kimi”)
        "kiminin",        # of some (people)
    ]

    __locativePronounList = [
        "burada",     # here
        "şurada",     # there (near)
        "orada",      # there (far)
        "burası",     # this place
        "şurası",     # that place (near)
        "orası",      # that place (far)
        "buraya",     # to here
        "şuraya",     # to there (near)
        "oraya",      # to there (far)
        "buradan",    # from here
        "şuradan",    # from there (near)
        "oradan",     # from there (far)
        "nerede",     # where
        "nereye",     # to where
        "nereden"     # from where
    ]

    __negativePronounList = [
        "hiç",       # none, not any
        "hiçbir",    # none, no one (used with a noun)
        "hiçbiri",   # none of them
        "hiçkimse",  # no one
        "hiçbirisi", # none of them (alternative form of "hiçbiri")
        "hiçbirini"  # none of them (accusative)
    ]


    @staticmethod
    def mapLexFeat(err):
        lexFeats = dict(other_abbr = None, other_typo = None, pronType = None, numType = None, reflex = None)
        resLexFeat = []

        # ABBREVIATION
        if err.errType == 'KI':
            lexFeats["other_abbr"] = True
            filtered_lexFeats = {k: v for k, v in lexFeats.items() if v is not None}
            resLexFeat.append(filtered_lexFeats)
        # SPELLING
        elif err.errType == 'YA':
            lexFeats["other_typo"] = True
            filtered_lexFeats = {k: v for k, v in lexFeats.items() if v is not None}
            resLexFeat.append(filtered_lexFeats)
        else:
            tokens = (err.corrText).split()
            for idx, token in enumerate(tokens):
                lexFeats = dict(other_abbr = None, other_typo = None, pronType = None, numType = None, reflex = None)

                # PRONTYPE
                if token in LexFeat.__pronList:
                    lexFeats["pronType"] = "Prs" # Personal
                elif token.startswith("birbir"):
                    lexFeats["pronType"] = "Rcp" # Reciprocal Pronoun
                elif token in LexFeat.__interrogativePronounList:
                    lexFeats["pronType"] = "Int" # Interrogative Pronoun, Determiner, Numeral, or Adverb
                elif token in LexFeat. __demonstrativePronounList:
                    lexFeats["pronType"] = "Dem" # Demonstrative Pronoun
                elif token in LexFeat.__indefinitePronounList:
                    lexFeats["pronType"] = "Ind" # Indefinite Pronoun
                elif token in LexFeat.__locativePronounList:
                    lexFeats["pronType"] = "Loc" # Locative Pronoun
                elif token in LexFeat.__negativePronounList:
                    lexFeats["pronType"] = "Neg" # Negative Determiner or Pronoun
                elif token == "bir":
                    lexFeats["pronType"] = "Art" # Article
                else:
                    lexFeats["pronType"] = None
                
                # NUMTYPE
                if "Card" in err.morphAnalysisFormatLong[idx] or token == "bir":
                    lexFeats["numType"] = "Card" # Cardinal Number
                elif "Ord" in err.morphAnalysisFormatLong[idx]:
                    lexFeats["numType"] = "Ord" # Ordinal Number
                elif "Dist" in err.morphAnalysisFormatLong[idx]:
                    lexFeats["numType"] = "Dist" # Distributive Numeral
                else:
                    lexFeats["numType"] = None
                
                # REFLEX
                if "Reflex" in err.morphAnalysisFormatLong[idx]:
                    lexFeats["reflex"] = "True"
                else:
                    lexFeats["reflex"] = None
                

                filtered_lexFeats = {k: v for k, v in lexFeats.items() if v is not None}
                resLexFeat.append(filtered_lexFeats)
                    
        return resLexFeat