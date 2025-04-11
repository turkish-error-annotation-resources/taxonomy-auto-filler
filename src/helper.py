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
from zemberek.morphology import TurkishMorphology # type: ignore


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
    def get_sentence_original(rawText, start, end):
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
    
    @staticmethod
    def get_corrected_sentence(idx, sentOrig, idxStartSent, idxEndSent):
        """
        returns the reconstructed correct sentence for a given original sentence
        """
        # sorting errors occured in the text according to the start (asc) and end (desc) index of the error
        errors_sorted = sorted(globals.data[idx]["annotations"][0]["result"], key = lambda e: (e["value"]["start"], -e["value"]["end"]))

        # only textarea type records are enough to process which contains corrected form
        errors_filtered_by_type = list(filter(lambda x: x["type"] == "textarea", errors_sorted))

        # for the errors which have the same start and end indices, it is enough to process only one of them becuase annotators wrote the resultant correct form for the same span
        # !!! errors with the same span should be identifed and revise to comply with this assumption !!!
        seen = set()
        errors_filtered_by_same_span = []
        for x in errors_filtered_by_type:
            key = (x['value']['start'], x['value']['end'])
            if key not in seen:
                seen.add(key)
                errors_filtered_by_same_span.append(x)
        
        # if there are overlapping errors, wider span will be processed, others are removed
        errors_filtered_by_overlapping_span = []
        for current in errors_filtered_by_same_span:
            cur_start = current['value']['start']
            cur_end = current['value']['end']

            # check if current is contained within any already-kept error
            is_contained = False
            for kept in errors_filtered_by_overlapping_span:
                kept_start = kept['value']['start']
                kept_end = kept['value']['end']

                if kept_start <= cur_start and cur_end <= kept_end:
                    is_contained = True
                    break

            if not is_contained:
                errors_filtered_by_overlapping_span.append(current)

        
        #if sentOrig == "Son olarak, insanların ülkeleri ve halkına faydalı olabilmesi sadece eğitim hayatlarında başarılı olmasından ibaret değil, belki insanların sıkıntılarının giderilmesi konusunda gece gündüz çalışması da oldukça önemlidir.":
        #    for error in errors_filtered_by_overlapping_span:
        #        print(error)

        # sent span -> 1089 & 1309
        # reconstruct the sentence by using corrected forms written by annotators
        offset = 0
        for error in errors_filtered_by_overlapping_span:
            if idxStartSent <= error["value"]["start"] and idxEndSent >= error["value"]["end"]:

                start = error["value"]["start"] - idxStartSent + offset
                end = error["value"]["end"] - idxStartSent + offset

                #if idxStartSent == 1089 and idxEndSent == 1309:
                    #print("sentOrig -> ", sentOrig)
                sentOrig = sentOrig[:start] + error["value"]["text"][0] + sentOrig[end:]
                offset += len(error["value"]["text"][0]) - (error["value"]["end"] - error["value"]["start"])

                #if idxStartSent == 1089 and idxEndSent == 1309:
                    #print("start:", start, " end:", end, " offset:", offset, " sentOrig:", sentOrig)
                
        return sentOrig 