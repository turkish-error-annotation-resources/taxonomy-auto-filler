
# Represents <Error> in the paper https://doi.org/10.1007/s10579-024-09794-0
class Error:
    # constructor
    def __init__(self, id = "", idLabelStudio = 0, idData = 0, rawText = '', idxStartErr = 0, idxEndErr = 0, incorrText = '', errType = '', corrText = '', errTax = None, metadata = None):    
        self.id = id # id of the result
        self.idLabelStudio = idLabelStudio # data[0]["id"] -> id that Label Studio assigned to task (text)
        self.idData = idData # data[0]["data"]["ID"] -> id that is coming from the data itself (per text)
        self.rawText = rawText # data[0]["data"]["DATA"] -> raw text of task
        self.idxStartErr = idxStartErr # data[0]["annotations"][0]["result"][0]["value"]["start"] -> index that the error starts
        self.idxEndErr = idxEndErr # data[0]["annotations"][0]["result"][0]["value"]["end"] -> index that the error ends
        self.incorrText = incorrText # data[0]["annotations"][0]["result"][0]["value"]["text"] -> incorrect text
        self.errType = errType # data[0]["annotations"][0]["result"][0]["value"]["labels"][0] -> type of the error (from an observational experience, it is known that Label Studio create different result object for the same region that has different label)
        self.corrText = corrText # data[0]["annotations"][0]["result"][1]["value"]["text"][0] -> corrected text, filled by Helper.get_corrected_text()
        self.errTax = errTax # for taxonomy mapping of the error
        self.metadata = metadata # for metadata
    
    def to_dict(self):
        return {
            "id": self.id,
            "idLabelStudio": self.idLabelStudio,
            "idData": self.idData,
            "rawText": self.rawText,
            "idxStartErr": self.idxStartErr,
            "idxEndErr": self.idxEndErr,
            "incorrText": self.incorrText,
            "errType": self.errType,
            "corrText": self.corrText,
            "errTax": self.errTax.to_dict() if self.errTax else None,
            "metadata": self.metadata.to_dict() if self.metadata else None
        }