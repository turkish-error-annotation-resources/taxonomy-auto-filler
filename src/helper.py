import globals
import json
import pandas as pd
from nltk.tokenize import sent_tokenize

class Helper:
    """ Helper functions used in main parsing loop """

    @staticmethod
    def load_data(path):
        try:
            with open(path, 'r') as file:
                globals.data = json.load(file)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise ValueError("An unexpected error occurred. ")
        
        if globals.debug:
            print("Number of tasks: ", len(globals.data))

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
    
    @staticmethod
    def load_abbr_list_TR():
        """ reads and get all abbreviations defined by TDK from the abbr_list_tr.xlsx file """

        try:
            df = pd.read_excel("./res/abbr_list_tr.xlsx")
            for row in df.values.tolist():
                globals.abbr_list_TR.append(str(row[0]).lower())
        except Exception as e:
            print(f"Error reading excel file: {e}")
    
    @staticmethod
    def get_sentence_errored(rawText, start, end):
        """
        returns the sentence which the errored region is in
        """

        sentences = sent_tokenize(rawText)

        # find the sentence that contains the indices
        for sentence in sentences:
            sentence_start = rawText.find(sentence)  # find the start index of the sentence in the original text
            sentence_end = sentence_start + len(sentence)  # calculate the end index of the sentence

            # check if the indices are within the current sentence
            if sentence_start <= start <= sentence_end or sentence_start <= end <= sentence_end:
                return sentence.strip(), sentence_start, sentence_end  # return the sentence if it contains the indices

        return "", -1, -1  # Return an empty string if no sentence is found