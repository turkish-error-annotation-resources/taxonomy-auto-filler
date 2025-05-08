import json

class Error:
    """ Represents <Error> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    def __init__(self, idLabelStudio = 0, idData = 0, rawText = '', idxStartErr = 0, idxEndErr = 0, sentOrig = '', idxStartSent = 0, idxEndSent = 0, sentCorr = '', errType = '', incorrText = '', corrText = '', errTax = None, morphAnalysisFormatLong = []):
        self.idLabelStudio = idLabelStudio # data[0]["id"] -> id that Label Studio assigned to task (text)
        self.idData = idData # data[0]["data"]["ID"] -> id that is coming from the data itself (per text)
        self.rawText = rawText # data[0]["data"]["DATA"] -> raw text of task
        self.idxStartErr = idxStartErr # data[0]["annotations"][0]["result"][0]["value"]["start"] -> index that the error starts
        self.idxEndErr = idxEndErr # data[0]["annotations"][0]["result"][0]["value"]["end"] -> index that the error ends
        self.sentOrig = sentOrig # sentence that the error is observed in, filled by Helper.get_sentence_original
        self.idxStartSent = idxStartSent # start idx (in text) of incorrect sentence that involves the error, filled by Helper.get_sentence_original()
        self.idxEndSent = idxEndSent # end idx (in text) of incorrect sentence that involves the error, filled by Helper.get_sentence_original()
        self.sentCorr = sentCorr # reconstructed sentence by corrections, filled by Helper.get_corrected_sentence()
        self.errType = errType # data[0]["annotations"][0]["result"][0]["value"]["labels"][0] -> type of the error (from an observational experience, it is known that Label Studio create different result object for the same region that has different label)
        self.incorrText = incorrText # data[0]["annotations"][0]["result"][0]["value"]["text"] -> incorrect text
        self.corrText = corrText # data[0]["annotations"][0]["result"][1]["value"]["text"][0] -> corrected text, filled by Helper.get_corrected_text()
        self.errTax = errTax # for taxonomy mapping of the error
        self.morphAnalysisFormatLong = morphAnalysisFormatLong # long format of the morph analysis by Zemberek, filled while inflectional feature analysis, used in lexical feature detection

    def to_dict(self):
        return {
            "idLabelStudio": self.idLabelStudio,
            "idData": self.idData,
            "rawText": self.rawText,
            "idxStartErr": self.idxStartErr,
            "idxEndErr": self.idxEndErr,
            "sentOrig": self.sentOrig,
            "idxStartSent": self.idxStartSent,
            "idxEndSent": self.idxEndSent,
            "sentCorr": self.sentCorr,
            "errType": self.errType,
            "incorrText": self.incorrText,
            "corrText": self.corrText,
            "errTax": self.errTax.to_dict() if self.errTax else None,
            "morphAnalysisFormatLong": json.dumps(self.morphAnalysisFormatLong) if self.morphAnalysisFormatLong else None
        }
        
    def print(self, errTypeList):
        """
        print errors in which provided by errTypeList
        if empty list is given as an input, prints all errors
        """
        if (self.errType in errTypeList) or (errTypeList == []):
            print('idData: ', self.idData)
            print('sentOrig: ', self.sentOrig)
            print('sentCorr: ', self.sentCorr)
            print('errType: ', self.errType)
            print('incorrText: ', self.incorrText)
            print('corrText: ', self.corrText)
            
            # taxonomy related features
            posResult = 'errTax.pos\t: ['
            for idx, item in enumerate(self.errTax.pos):
                posResult += str(item)
                if idx != len(self.errTax.pos) - 1:
                    posResult += ', '
            posResult += ']'
            print('\033[31m', posResult, '\033[0m')

            print('\033[31m', 'errTax.unit\t: ', self.errTax.unit, '\033[0m')
            print('\033[31m', 'errTax.phenomenon: ', self.errTax.phenomenon, '\033[0m')
            print('\033[31m', 'errTax.level\t: ', self.errTax.level, '\033[0m')
            print('\033[31m', 'errTax.infFeat: ', [{k: v for k, v in d.items() if v is not None} for d in self.errTax.infFeat], '\033[0m') # to show attributes only have values
            print('\033[31m', 'errTax.lexFeat: ',self.errTax.lexFeat, '\033[0m')
                
            print()