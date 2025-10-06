from model.error_tag import ErrorTag
from nltk.tokenize import wordpunct_tokenize

# Represents <LexicalFeature> in the paper https://doi.org/10.1007/s10579-024-09794-0
class LexFeat():

    # from Universal Dependencies web platform https://universaldependencies.org/u/feat/index.html (accessed on 2025-09-13)
    LEXICAL_FEATURES = {"PronType", "NumType", "Poss", "Reflex"}
    OTHER_FEATURES = {"Abbr", "Typo", "Foreign", "ExtPos"}

    @staticmethod
    def mapLexFeat(err, line_list, overlap_flag):
        if err.errType in [ErrorTag.NO.value, ErrorTag.SI.value, ErrorTag.ÇA.value, ErrorTag.ZA.value, ErrorTag.KİP.value,
                            ErrorTag.GÖ.value, ErrorTag.OL.value, ErrorTag.ŞA.value, ErrorTag.ÇF.value, ErrorTag.SE.value, 
                            ErrorTag.KK.value, ErrorTag.GE.value, ErrorTag.ST.value, ErrorTag.TÜ.value, ErrorTag.AB.value, 
                            ErrorTag.KEG.value, ErrorTag.KBF.value, ErrorTag.İB.value, ErrorTag.AnB.value, ErrorTag.ÜS.value, 
                            ErrorTag.DİJ.value]:
            return []
        elif err.errType == ErrorTag.YA.value:
            return [(err.corrText, "Typo=Yes")] # format: (FORM, FEATS)
        elif err.errType == ErrorTag.KI.value:
            return [(err.corrText, "Abbr=Yes")] # format: (FORM, FEATS)
        else:
            result = []
            if overlap_flag:
                tokens = wordpunct_tokenize(err.corrText)

                for token in tokens:
                    st_idx = 0
                    ed_idx = 0
                    multi_token_flag = False

                    for line in line_list:
                        cols = line.split("\t")

                        # if the multi-token flag is on, then keep adding lines until the end index is reached
                        if multi_token_flag:
                            if int(cols[0]) <= ed_idx:
                                # format: (FORM, FEATS)
                                result.append((cols[1], cols[5]))
                                if int(cols[0]) == ed_idx:
                                    multi_token_flag = False
                            else:
                                multi_token_flag = False

                        if cols[1] == token:
                            # format: (FORM, FEATS)
                            result.append((cols[1], cols[5]))
                            
                            # if it is multi-token, then keep start and end indices and switch the flag
                            if "-" in cols[0]:
                                multi_token_flag = True
                                st_idx, ed_idx = cols[0].split("-")
                                st_idx = int(st_idx)
                                ed_idx = int(ed_idx)
            else:
                for line in line_list:
                    cols = line.split("\t")
                    # format: (FORM, FEATS)
                    result.append((cols[1], cols[5]))

            # filtering only lexical features
            res_filtered = []
            for item in result:
                feats = item[1].split("|")
                res = ""
                for feat in feats:
                    if feat.startswith(tuple(LexFeat.LEXICAL_FEATURES)) or feat.startswith(tuple(LexFeat.OTHER_FEATURES)):
                        res += feat + "|"
                res_filtered.append((item[0], res[:-1])) # removing the last "|"
            
            return res_filtered