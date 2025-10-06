from model.error_tag import ErrorTag
from nltk.tokenize import wordpunct_tokenize

# Represents <InflectionalFeature> in the paper https://doi.org/10.1007/s10579-024-09794-0
class InfFeat():

    # from Universal Dependencies web platform https://universaldependencies.org/u/feat/index.html (accessed on 2025-09-13)
    INFLECTIONAL_FEATURES = {"Gender", "Animacy", "NounClass", "Number", "Case", "Definite", "Deixis", "DeixisRef", "Degree", 
                        "VerbForm", "Mood", "Tense", "Aspect", "Voice", "Evident", "Polarity", "Person", "Polite", "Clusivity"}

    @staticmethod
    def mapInfFeat(err, line_list, overlap_flag):
        if err.errType in [ErrorTag.NO.value, ErrorTag.BH.value, ErrorTag.Dİ.value, ErrorTag.KI.value, ErrorTag.ÜDü.value, 
                            ErrorTag.ÜDa.value, ErrorTag.ÜzT.value, ErrorTag.SI.value, ErrorTag.SE.value, ErrorTag.KK.value, 
                            ErrorTag.GE.value, ErrorTag.ST.value, ErrorTag.TÜ.value, ErrorTag.İB.value, ErrorTag.AnB.value, 
                            ErrorTag.ÜS.value, ErrorTag.DİJ.value]:
            return []
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
            
            # filtering only inflectional features
            res_filtered = []
            for item in result:
                feats = item[1].split("|")
                res = ""
                for feat in feats:
                    if feat.startswith(tuple(InfFeat.INFLECTIONAL_FEATURES)):
                        res += feat + "|"
                res_filtered.append((item[0], res[:-1])) # removing the last "|"
            
            return res_filtered