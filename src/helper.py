import globals

class Helper:
    """ Helper functions used in main parsing loop """

    @staticmethod
    def get_corrected_text(idx, resultId):
        """ takes index (task id) and result (annotation) id to return the corrected form for the error """
        
        for res in globals.data[idx]["annotations"][0]["result"]:
            if res["id"] == resultId and res["type"] == "textarea":
                return res["value"]["text"][0]