from model.error_tag import ErrorTag
from nltk.tokenize import wordpunct_tokenize
import sys

# Represents <Part-of-speech> in the paper https://doi.org/10.1007/s10579-024-09794-0
# important: POS results are returned as a list of tuples (UPOS, XPOS)
class POS:
    
    @staticmethod
    def mapPOS(err, line_list, overlap_flag):
        if err.errType in [ErrorTag.SI.value, ErrorTag.SE.value, ErrorTag.SH.value, ErrorTag.İB.value, ErrorTag.AnB.value,
                            ErrorTag.ÜS.value, ErrorTag.DİJ.value]:
            return []
        elif err.errType == ErrorTag.NO.value:
            return [(err.corrText, "PUNCT", "")]
        elif err.errType == ErrorTag.KEG.value:
            return [(err.corrText, "VERB", "")]
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
                                # format: (FORM, POS, XPOS)
                                result.append((cols[1], cols[3], cols[4]))
                                if int(cols[0]) == ed_idx:
                                    multi_token_flag = False
                            else:
                                multi_token_flag = False

                        if cols[1] == token:
                            # format: (FORM, POS, XPOS)
                            result.append((cols[1], cols[3], cols[4]))
                            
                            # if it is multi-token, then keep start and end indices and switch the flag
                            if "-" in cols[0]:
                                multi_token_flag = True
                                st_idx, ed_idx = cols[0].split("-")
                                st_idx = int(st_idx)
                                ed_idx = int(ed_idx)
            else:
                for line in line_list:
                    cols = line.split("\t")
                    # format: (FORM, POS, XPOS)
                    result.append((cols[1], cols[3], cols[4]))
            
            return result