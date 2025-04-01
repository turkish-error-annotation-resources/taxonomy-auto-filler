class Error:
    def __init__(self, idLabelStudio = 0, idData = 0, rawText = '', sentOrig = '', sentCorr = '', idxStartErr = 0, idxEndErr = 0, errType = '', incorrText = '', corrText = '', idxStartSent = 0, idxEndSent = 0, errTax = None):
        self.idLabelStudio = idLabelStudio # data[0]["id"] -> id that Label Studio assigned to task (text)
        self.idData = idData # data[0]["data"]["ID"] -> id that is coming from the data itself (per text)
        self.rawText = rawText # data[0]["data"]["DATA"] -> raw text of task
        self.sentOrig = sentOrig # get_sentence_by_index(data[0]["data"]["DATA"], data[0]["annotations"][0]["result"][0]["value"]["start"]) -> sentence that the error is observed in
        self.sentCorr = sentCorr # corrected sentence ???
        self.idxStartErr = idxStartErr # data[0]["annotations"][0]["result"][0]["value"]["start"] -> index that the error starts
        self.idxEndErr = idxEndErr # data[0]["annotations"][0]["result"][0]["value"]["end"] -> index that the error ends
        self.errType = errType # data[0]["annotations"][0]["result"][0]["value"]["labels"][0] -> type of the error
        self.incorrText = incorrText # data[0]["annotations"][0]["result"][0]["value"]["text"] -> incorrect text
        self.corrText = corrText # data[0]["annotations"][0]["result"][1]["value"]["text"][0] -> corrected text
        self.idxStartSent = idxStartSent # start idx of incorrect sentence that involves the error ???
        self.idxEndSent = idxEndSent # end idx of incorrect sentence that involves the error ???
        self.errTax = errTax # taxonomic representation of the error

    def print(self):
        print('idData: ', self.idData)
        print('sentOrig: ', self.sentOrig)
        print('sentCorr: ', self.sentCorr)
        print('idxStartErr: ', self.idxStartErr)
        print('idxEndErr: ', self.idxEndErr)
        print('errType: ', self.errType)
        print('errTax.pos: ', self.errTax.pos)
        print('errTax.unit: ', self.errTax.unit)
        print('errTax.phenomenon: ', self.errTax.phenomenon)
        print('errTax.level: ', self.errTax.level)
        print()