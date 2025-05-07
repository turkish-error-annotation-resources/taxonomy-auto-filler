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
from zemberek.tokenization import TurkishTokenizer # type: ignore
from zemberek.tokenization import TurkishSentenceExtractor # type: ignore

import functools
import Levenshtein


class Helper:
    """ Helper static functions """

    __tokenizer = TurkishTokenizer.DEFAULT
    __morphology = TurkishMorphology.createWithDefaults()
    __extractor = TurkishSentenceExtractor.DEFAULT


    @staticmethod
    def get_morphology():
        return Helper.__morphology

    @staticmethod
    def get_tokenizer():
        return Helper.__tokenizer
    
    @staticmethod
    def get_extractor():
        """
        used in Helper.get_sentence_original()
        """
        return Helper.__extractor
 
    @staticmethod
    def load_data(path):
        """
        loading Label Studio's json output/export file given as a path
        used in main
        """
        try:
            with open(path, 'r') as file:
                globals.data = json.load(file)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise ValueError("An unexpected error occurred.")
        
        if globals.debug:
            print("Number of tasks in the input file: ", len(globals.data))
        
    @staticmethod
    def load_abbr_list_TR():
        """ 
        reads and get all abbreviations defined by TDK from the abbr_list_tr.xlsx file and loads globals.abbr_list_TR list
        used in main
        """
        try:
            df = pd.read_excel("./res/abbr_list_tr.xlsx")
            for row in df.values.tolist():
                globals.abbr_list_TR.append(str(row[0]).lower())
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def get_sentence_original(rawText, start, end):
        """
        returns the sentence which the errored region is in
        used in main
        """
        extracted_sentences = Helper.get_extractor().fromParagraph(rawText)
        sentences = []
        for sentence in extracted_sentences:
            sentences.append(str(sentence))

        for sentence in sentences: # find the sentence that contains the indices
            sentence_start = rawText.find(sentence)  # find the start index of the sentence in the original text
            sentence_end = sentence_start + len(sentence)  # calculate the end index of the sentence

            # check if the indices are within the current sentence
            if sentence_start <= start <= sentence_end or sentence_start <= end <= sentence_end:
                return sentence.strip(), sentence_start, sentence_end  # return the sentence if it contains the indices
            
        return "", -1, -1  # return an empty string if no sentence is found

    @staticmethod
    def get_corrected_sentence(idx, sentOrig, idxStartSent, idxEndSent):
        """
        returns the reconstructed correct sentence for a given original sentence
        used in main
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

        # reconstruct the sentence by using corrected forms written by annotators
        offset = 0
        for error in errors_filtered_by_overlapping_span:
            if idxStartSent <= error["value"]["start"] and idxEndSent >= error["value"]["end"]:

                start = error["value"]["start"] - idxStartSent + offset
                end = error["value"]["end"] - idxStartSent + offset

                sentOrig = sentOrig[:start] + error["value"]["text"][0] + sentOrig[end:]
                offset += len(error["value"]["text"][0]) - (error["value"]["end"] - error["value"]["start"])
                
        return sentOrig

    @staticmethod
    def get_corrected_text(idx, resultId):
        """
        takes index (task id) and result (annotation) id to return the corrected form for the error
        used in main
        """
        for res in globals.data[idx]["annotations"][0]["result"]:
            if res["id"] == resultId and res["type"] == "textarea":
                return res["value"]["text"][0]



















    




    
    
    

    
    
    @staticmethod
    def extract_punctuation_marks_TR(text):
        """ finds and returns all punctiation marks in the input text as a list """

        punctiation_marks_TR = ['.', ',', ':', ';', '?', '!', '/' '\'', '-', '—', '…', '(', ')', '[', ']', '"', "'", "`", "´" 'ʺ'] # 17 punctioation marks in Turkish defined by TDK (plus ` and ´)
        return [char for char in text if char in punctiation_marks_TR]
    
    
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
    def find_sublist_range(lst1, lst2):
        n, m = len(lst1), len(lst2)
        for i in range(n - m + 1):
            if lst1[i:i + m] == lst2:
                return (i, i + m)
        return (0, 0)  # if no match

    @staticmethod
    def get_POS(sent, corrText):
        morph = Helper.get_morphology()
        try:
            # get analysis and best disambiguation result for the corrected sentence
            results = morph.analyzeSentence(sent)
            results_disambiguated = morph.disambiguate(sent, results)
            best = results_disambiguated.bestAnalysis()

            # get analysis and best disambiguation result for the corrected text
            results_corrTxt = morph.analyzeSentence(corrText)
            results_disambiguated_corrTxt = morph.disambiguate(corrText, results_corrTxt)
            best_corrTxt = results_disambiguated_corrTxt.bestAnalysis()

            
            surface_forms = [a.surfaceForm() for a in best]
            surface_forms_corrTxt = [a.surfaceForm() for a in best_corrTxt]

            start, end = Helper.find_sublist_range(surface_forms, surface_forms_corrTxt)

            res = []
            for idx, token in enumerate(best):
                if idx in range(start, end):
                    #print(token.getPos())
                    posRecord = dict(posPrimary = str(token.getPos()), posSecondary = str(token.getDictionaryItem().secondaryPos), surfaceForm = str(token.surfaceForm()))
                    #res.append(str(token.getPos()))
                    res.append(posRecord)
        except Exception as e:
            #print(e)
            return []
        else:
            return res
        
    @staticmethod
    def get_morpholocial_analysis(err):
        """
        returns the best analysis for the corrected text
        """
        morph = Helper.get_morphology()
        try:
            if err.sentCorr.strip() == "":
                return []
            # get analysis and the best disambiguation result for the corrected sentence
            results = morph.analyzeSentence(err.sentCorr)
            results_disambiguated = morph.disambiguate(err.sentCorr, results)
            best = results_disambiguated.bestAnalysis()

            
            if err.corrText.strip() == "":
                return []
            # get analysis and best disambiguation result for the corrected text
            results_corrTxt = morph.analyzeSentence(err.corrText)
            results_disambiguated_corrTxt = morph.disambiguate(err.corrText, results_corrTxt)
            best_corrTxt = results_disambiguated_corrTxt.bestAnalysis()
            


            surface_forms = [a.surfaceForm() for a in best]
            surface_forms_corrTxt = [a.surfaceForm() for a in best_corrTxt]

            start, end = Helper.find_sublist_range(surface_forms, surface_forms_corrTxt)

            res = []
            for idx, token in enumerate(best):
                if idx in range(start, end):
                    res.append(token)
        except Exception as e:
            if globals.debug:
                print("err.sentCorr: ", err.sentCorr)
                print("err.corrText: ", err.corrText)
                print("err.errType: ", err.errType)
                print(e)
            return []
        else:
            return res

    # !!! not used for now !!!
    @staticmethod
    def morph_align_by_levenshtein(morphemes, word):
        
        @functools.lru_cache(maxsize = None)
        def dp(m_idx, w_idx):
            
            # Eğer morfemler de kelime de bitti: Tam hizalama
            if m_idx == len(morphemes) and w_idx == len(word):
                return [], 0
            
            options = []

            # 1. Morfem varsa ve segment eşleştirilebilirse
            if m_idx < len(morphemes):
                
                morph = morphemes[m_idx]
                for end in range(w_idx + 1, len(word) + 1):# 1 - 7 -> 2 - 7 -> 3 - 7
                    segment = word[w_idx:end] # y -> '' -> ''
                    dist = Levenshtein.distance(morph, segment) # 2 -> 3 ->
                    sub_align, sub_cost = dp(m_idx + 1, end)
                    options.append(([(morph, segment, dist)] + sub_align, dist + sub_cost))
                    #print("1 ->", options[len(options)-1])

                # 2. Morfemi atla (boş eşleşme) — buna küçük bir ceza ekle (örneğin 1)
                sub_align, sub_cost = dp(m_idx + 1, w_idx)
                options.append(([(morph, "", len(morph))] + sub_align, len(morph) + sub_cost))
                #print("2 ->", options[len(options)-1])

            # 3. Kelimede segment kaldıysa ama morfem yoksa — kelimeyi atla
            if w_idx < len(word):
                sub_align, sub_cost = dp(m_idx, w_idx + 1)
                options.append(([(None, word[w_idx], 1)] + sub_align, 1 + sub_cost))
                #print("3 ->", options[len(options)-1])

            # En düşük maliyetli seçeneği döndür
            return min(options, key=lambda x: x[1])

        return dp(0, 0)