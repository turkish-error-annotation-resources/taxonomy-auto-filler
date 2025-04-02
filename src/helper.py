import globals
import json
import pandas as pd
from nltk.tokenize import sent_tokenize
# for zemberek
import jpype
import jpype.imports
from jpype.types import *
# Start JVM with Zemberek
if not jpype.isJVMStarted():
    jpype.startJVM(classpath = [globals.path_zemberek])
from zemberek.morphology import TurkishMorphology


class Helper:
    """ Helper functions used in main parsing loop """

    __morphology = TurkishMorphology.createWithDefaults()

    @staticmethod
    def get_morphology():
        return Helper.__morphology

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
        for sentence in sentences: # find the sentence that contains the indices
            sentence_start = rawText.find(sentence)  # find the start index of the sentence in the original text
            sentence_end = sentence_start + len(sentence)  # calculate the end index of the sentence

            # check if the indices are within the current sentence
            if sentence_start <= start <= sentence_end or sentence_start <= end <= sentence_end:
                return sentence.strip(), sentence_start, sentence_end  # return the sentence if it contains the indices
            
        return "", -1, -1  # return an empty string if no sentence is found
    
    
    @staticmethod
    def get_lemmas(word):
        """
        get analysis of an input word using zemberek's morphological analyzer
        analysis may have more than one result, but one should be chosen
        heuristic: choose the lemma which has the smallest length
        !!! better approach -> using morpholocial disambiguator
        """

        morph = Helper.get_morphology()
        analysis = morph.analyze(word)
        lemmas = set()
        for result in analysis:
            lemmas.update(result.getLemmas())

        lemmas = list(lemmas)
        
        if len(lemmas) == 0: # no analysis
            return ""
        else:
            return min(lemmas, key=len)