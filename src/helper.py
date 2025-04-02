import globals

class Helper:
    """ Helper functions used in main parsing loop """

    @staticmethod
    def get_corrected_text(idx, resultId):
        """ takes index (task id) and result (annotation) id to return the corrected form for the error """
        
        for res in globals.data[idx]["annotations"][0]["result"]:
            if res["id"] == resultId and res["type"] == "textarea":
                return res["value"]["text"][0]
    
    @staticmethod
    def extract_punctuation_marks_TR(text):
        """ finds and returns all punctiation marks in the input text as a list """
        
        punctiation_marks_TR = ['.', ',', ':', ';', '?', '!', '/' '\'', '-', '—', '…', '(', ')', '[', ']', '"', "'", "`", "´" 'ʺ'] # 17 punctioation marks in Turkish defined by TDK (plus ` and ´)
        return [char for char in text if char in punctiation_marks_TR]