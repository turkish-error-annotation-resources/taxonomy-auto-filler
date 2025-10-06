from enum import Enum
from helper import Helper
from collections import Counter
from model.error_tag import ErrorTag
import nltk
from nltk.tokenize import wordpunct_tokenize

# Represents <Phenomenon> in the paper https://doi.org/10.1007/s10579-024-09794-0
class Phenomenon(Enum):
    
    NONE = 'None'
    OMISSION = 'Omission' # the absence of an item that must appear in a well-formed utterance
    ADDITION = 'Addition' # the presence of an item that should not appear in a well-formed utterance
    MISUSE = 'Misuse' # the use of the wrong form of the morpheme or structure
    MISORDERING = 'Misordering' # the incorrect placement of a morpheme or a group of morphemes in an utterance
    UNTRANSLATED = 'Untranslated' # not used
    AMBIGUITY = 'Ambiguity'

    @staticmethod
    def mapPhenomenon(err, line_list, overlap_flag):
        if err.errType in [ErrorTag.BH.value, ErrorTag.KI.value, ErrorTag.ÜzY.value, ErrorTag.ÜDü.value, ErrorTag.ÜU.value, 
                            ErrorTag.ÜzB.value, ErrorTag.ÜDa.value, ErrorTag.ÜzT.value, ErrorTag.ZA.value, ErrorTag.GÖ.value,
                            ErrorTag.ŞA.value, ErrorTag.ÇF.value, ErrorTag.ST.value, ErrorTag.AB.value, ErrorTag.İB.value,
                            ErrorTag.ÜS.value]:
            return Phenomenon.MISUSE
        elif err.errType == ErrorTag.SI.value:
            return Phenomenon.MISORDERING
        elif err.errType == ErrorTag.GE.value:
            return Phenomenon.ADDITION
        elif err.errType in [ErrorTag.KEG.value, ErrorTag.KBF.value]:
            return Phenomenon.OMISSION
        elif err.errType == ErrorTag.AnB.value:
            return Phenomenon.AMBIGUITY
        elif err.errType == ErrorTag.DİJ.value:
            return Phenomenon.NONE
        elif err.errType == ErrorTag.NO.value:
            # heuristical approach:  using th change in the number of punctiation marks
            # if lengths of pnct. marks lists are equal, then there are two options: 
            #   1- at least one element which is different -> MISUSE
            #   2- no different element -> MISORDERING
            # if there are more punct. marks in corrected form than in the original form -> OMISSION
            # if there are less punct. marks in corrected form than in the original form -> ADDITION
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
        elif err.errType == ErrorTag.YA.value:
            # if frequency of each character for both texts are equal -> MISORDERING
            # if length of the original text is greater than the corrected text -> ADDITION
            # if length of the original text is smaller than the corrected text -> OMISSION
            # otherwise -> MISUSE
            if (dict(Counter(err.incorrText)) == dict(Counter(err.corrText))):
                return Phenomenon.MISORDERING
            elif len(err.incorrText) > len(err.corrText):
                return Phenomenon.ADDITION
            elif len(err.incorrText) < len(err.corrText):
                return Phenomenon.OMISSION
            else:
                return Phenomenon.MISUSE
        elif err.errType == ErrorTag.BA.value:
            # if unnecessary spaces are inserted within a single word -> ADDITION, else OMMISSION
            if len(err.incorrText.split()) > 1:
                return Phenomenon.ADDITION
            else:
                return Phenomenon.OMISSION
        elif err.errType == ErrorTag.Dİ.value:
            # set operations are used heuristically, it can be improved by different approaches (using character frequency dictionary, etc.)
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
        elif err.errType in [ErrorTag.KH.value, ErrorTag.DU.value]:
            # TODO: incorrect text is assumed that it involves only one error
            # compare err.incorrText and err.corrText
            if len(err.incorrText) > len(err.corrText):
                return Phenomenon.ADDITION
            elif len(err.incorrText) < len(err.corrText):
                return Phenomenon.OMISSION
            elif len(err.incorrText) == len(err.corrText):
                return Phenomenon.MISUSE
        elif err.errType == ErrorTag.DU.value:
            # it is assumed that selected span with this error has only one token, if not -> returns MISUSE by default!
            if len(err.incorrText.split()) > 1:
                return Phenomenon.MISUSE
            else:
                if len(err.incorrText) > len(err.corrText):
                    return Phenomenon.ADDITION
                elif len(err.incorrText) < len(err.corrText):
                    return Phenomenon.OMISSION
                else:
                    return Phenomenon.MISUSE
        elif err.errType == ErrorTag.KK.value:
            if "ki" in err.incorrText.strip()[-2:].lower() or "kı" in err.incorrText.strip()[-2:].lower():
                return Phenomenon.ADDITION

            if len(err.incorrText) > len(err.corrText):
                return Phenomenon.ADDITION
            elif len(err.incorrText) < len(err.corrText):
                return Phenomenon.OMISSION
            else:
                return Phenomenon.NONE
        elif err.errType in [ErrorTag.SA.value, ErrorTag.SE.value]:
            if len(err.incorrText) > len(err.corrText):
                return Phenomenon.ADDITION
            elif len(err.incorrText) < len(err.corrText):
                return Phenomenon.OMISSION
            else:
                return Phenomenon.NONE
            
        elif err.errType == ErrorTag.İY.value:
            # it is assumed that selected span with this error has only one token, if not -> returns MISUSE by default!
            if len(err.incorrText.split()) > 1:
                return Phenomenon.MISUSE
            else:
                url, payload = Helper.setup_udpipe2_call()
                service_result_incorrText = Helper.call_udpipe_service(err.incorrText, url, payload)
                
                isPsorExist = False
                for line in service_result_incorrText.splitlines():
                    cols = line.split("\t")
                    if len(cols) != 10:
                        continue
                    token_id = cols[0] # according to conllu format
                    feats = cols[5] # to process TokenRange attribute
                    
                    if "Person[psor]" in feats:
                        isPsorExist = True
                        break
                                
                featList = []
                if overlap_flag:
                    tokens = wordpunct_tokenize(err.corrText)

                    for token in tokens:
                        multi_token_flag = False

                        for line in line_list:
                            cols = line.split("\t")
                            
                            # if the multi-token flag is on, then keep adding lines until the end index is reached
                            if multi_token_flag:
                                featList.append(cols[5])
                                multi_token_flag = False

                            if cols[1].lower() == token.lower():
                                if "-" in cols[0]:
                                    multi_token_flag = True
                                else:
                                    featList.append(cols[5])
                else:
                    for line in line_list:
                        cols = line.split("\t")
                        featList.append(cols[5])

                isPsorExistInCorrText = False
                for item in featList:
                    if "Person[psor]" in item:
                        isPsorExistInCorrText = True
                        break

                if (isPsorExist and isPsorExistInCorrText) or (len(err.incorrText) == len(err.corrText)):
                    return Phenomenon.MISUSE
                if len(err.incorrText) > len(err.corrText):
                    return Phenomenon.ADDITION
                elif len(err.incorrText) < len(err.corrText):
                    return Phenomenon.OMISSION
        elif err.errType == ErrorTag.ÇA.value:
            # it is assumed that selected span with this error has only one token, if not -> returns MISUSE by default!
            if len(err.incorrText.split()) > 1:
                return Phenomenon.MISUSE
            else:
                url, payload = Helper.setup_udpipe2_call()
                service_result_incorrText = Helper.call_udpipe_service(err.incorrText, url, payload)
                
                isVoiceExist = False
                for line in service_result_incorrText.splitlines():
                    cols = line.split("\t")
                    if len(cols) != 10:
                        continue
                    token_id = cols[0] # according to conllu format
                    feats = cols[5] # to process TokenRange attribute
                    
                    if "Voice" in feats:
                        isVoiceExist = True
                        break
                
                featList = []
                if overlap_flag:
                    tokens = wordpunct_tokenize(err.corrText)

                    for token in tokens:
                        multi_token_flag = False

                        for line in line_list:
                            cols = line.split("\t")
                            
                            # if the multi-token flag is on, then keep adding lines until the end index is reached
                            if multi_token_flag:
                                featList.append(cols[5])
                                multi_token_flag = False

                            if cols[1].lower() == token.lower():
                                if "-" in cols[0]:
                                    multi_token_flag = True
                                else:
                                    featList.append(cols[5])
                else:
                    for line in line_list:
                        cols = line.split("\t")
                        featList.append(cols[5])
                
                isVoiceExistInCorrText = False
                for item in featList:
                    if "Voice" in item:
                        isVoiceExistInCorrText = True
                        break
                
                if (isVoiceExist and isVoiceExistInCorrText) or (len(err.incorrText) == len(err.corrText)):
                    return Phenomenon.MISUSE
                if len(err.incorrText) > len(err.corrText):
                    return Phenomenon.ADDITION
                elif len(err.incorrText) < len(err.corrText):
                    return Phenomenon.OMISSION
        elif err.errType == ErrorTag.KİP.value:
            # it is assumed that selected span with this error has only one token, if not -> returns MISUSE by default!
            if len(err.incorrText.split()) > 1:
                return Phenomenon.MISUSE
            else:
                url, payload = Helper.setup_udpipe2_call()
                service_result_incorrText = Helper.call_udpipe_service(err.incorrText, url, payload)
                
                isMoodExist = False
                for line in service_result_incorrText.splitlines():
                    cols = line.split("\t")
                    if len(cols) != 10:
                        continue
                    token_id = cols[0] # according to conllu format
                    feats = cols[5] # to process TokenRange attribute
                    
                    if "Mood" in feats:
                        isMoodExist = True
                        break
                
                featList = []
                if overlap_flag:
                    tokens = wordpunct_tokenize(err.corrText)

                    for token in tokens:
                        multi_token_flag = False

                        for line in line_list:
                            cols = line.split("\t")
                            
                            # if the multi-token flag is on, then keep adding lines until the end index is reached
                            if multi_token_flag:
                                featList.append(cols[5])
                                multi_token_flag = False

                            if cols[1].lower() == token.lower():
                                if "-" in cols[0]:
                                    multi_token_flag = True
                                else:
                                    featList.append(cols[5])
                else:
                    for line in line_list:
                        cols = line.split("\t")
                        featList.append(cols[5])
                
                isMoodExistInCorrText = False
                for item in featList:
                    if "Mood" in item:
                        isMoodExistInCorrText = True
                        break
                
                if (isMoodExist and isMoodExistInCorrText) or (len(err.incorrText) == len(err.corrText)):
                    return Phenomenon.MISUSE
                if len(err.incorrText) > len(err.corrText):
                    return Phenomenon.ADDITION
                elif len(err.incorrText) < len(err.corrText):
                    return Phenomenon.OMISSION
        elif err.errType == ErrorTag.OL.value:
            # it is assumed that selected span with this error has only one token, if not -> returns MISUSE by default!
            if len(err.incorrText.split()) > 1:
                return Phenomenon.MISUSE
            else:
                url, payload = Helper.setup_udpipe2_call()
                service_result_incorrText = Helper.call_udpipe_service(err.incorrText, url, payload)
                
                isPolarityExist = False
                for line in service_result_incorrText.splitlines():
                    cols = line.split("\t")
                    if len(cols) != 10:
                        continue
                    token_id = cols[0] # according to conllu format
                    feats = cols[5] # to process TokenRange attribute
                    
                    if "Polarity" in feats:
                        isPolarityExist = True
                        break
                
                featList = []
                if overlap_flag:
                    tokens = wordpunct_tokenize(err.corrText)

                    for token in tokens:
                        multi_token_flag = False

                        for line in line_list:
                            cols = line.split("\t")
                            
                            # if the multi-token flag is on, then keep adding lines until the end index is reached
                            if multi_token_flag:
                                featList.append(cols[5])
                                multi_token_flag = False

                            if cols[1].lower() == token.lower():
                                if "-" in cols[0]:
                                    multi_token_flag = True
                                else:
                                    featList.append(cols[5])
                else:
                    for line in line_list:
                        cols = line.split("\t")
                        featList.append(cols[5])

                isPolarityExistInCorrText = False
                for item in featList:
                    if "Polarity" in item:
                        isPolarityExistInCorrText = True
                        break
                
                if (isPolarityExist and isPolarityExistInCorrText) or (len(err.incorrText) == len(err.corrText)):
                    return Phenomenon.MISUSE
                if len(err.incorrText) > len(err.corrText):
                    return Phenomenon.ADDITION
                elif len(err.incorrText) < len(err.corrText):
                    return Phenomenon.OMISSION
        elif err.errType == ErrorTag.TÜ.value:
            if len(err.incorrText) > len(err.corrText):
                return Phenomenon.ADDITION
            elif len(err.incorrText) < len(err.corrText):
                return Phenomenon.OMISSION
            else:
                return Phenomenon.MISUSE # assumption: incorrect and correct word have the same length
        elif err.errType == ErrorTag.SH.value:
            if len(err.corrText.split()) == 0:
                return Phenomenon.ADDITION
            elif len(err.corrText.split()) > len(err.incorrText.split()):
                return Phenomenon.OMISSION
            else:
                return Phenomenon.MISUSE