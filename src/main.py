import argparse
import globals
from model.error import Error
from model.taxonomy import Taxonomy
from model.level import Level
from model.phenomenon import Phenomenon
from model.unit import Unit
from model.pos import POS
from model.inflectional_feature import InfFeat
from model.lexical_feature import LexFeat
from helper import Helper

import csv

def entry(path):
    
    Helper.load_data(path) # loading input file (Label Studio's json output/export file)
    Helper.load_abbr_list_TR() # loading TDK's abbreviation list into globals.abbr_list_TR list to be used in Unit detection for HN (PUNCTUATION)

    #sentence_pairs = [] # for parallel data extraction

    errorList = []
    for idx, task in enumerate(globals.data): # for each task in input json data
        for result in task["annotations"][0]["result"]: # annotators were informed that they should create only one "annotation" object in Label Studio (task["annotations"][0] usage is secured because of this assumption)
            if result["type"] == "labels": # there are two types of results: "labels" (contains error type) and "textarea" (contains corrected form)
                # creating an Error instance and filling the properties
                err = Error()
                err.idLabelStudio = task["id"] # id that Label Studio assigned to task (text)
                err.idData = task["data"]["ID"] # id that is coming from the data itself (per text)
                err.rawText = task["data"]["DATA"] # raw text of task
                err.idxStartErr = result["value"]["start"] # index that the error starts
                err.idxEndErr = result["value"]["end"] # index that the error starts
                err.sentOrig, err.idxStartSent, err.idxEndSent = Helper.get_sentence_original(err.rawText, err.idxStartErr, err.idxEndErr) # sentence that the error is observed in
                err.sentCorr = Helper.get_corrected_sentence(idx, err.sentOrig, err.idxStartSent, err.idxEndSent) # reconstructed sentence by corrections
                err.errType = result["value"]["labels"][0] # type of the error (from an observational experience, it is known that Label Studio create different result object for the same region that has different label)
                err.incorrText = result["value"]["text"] # incorrect text
                err.corrText = Helper.get_corrected_text(idx, result["id"]) # corrected text
                
                #sentence_pairs.append((err.idData, err.sentOrig, err.sentCorr)) # for parallel data extraction

                # taxonomy related features
                
                err.errTax = Taxonomy()
                err.errTax.pos = POS.mapPOS(err)
                err.errTax.unit = Unit.mapUnit(err)
                err.errTax.phenomenon = Phenomenon.mapPhenomenon(err)
                err.errTax.level = Level.mapLevel(err)
                err.errTax.infFeat = InfFeat.mapInfFeat(err)
                err.errTax.lexFeat = LexFeat.mapLexFeat(err)
                
                errorList.append(err)

                if globals.debug:
                    err.print([])
                    #err.print(["HN", "BA", "Dİ", "BH", "KI", "YA"])
                    #err.print(["ÜzY", "ÜU", "ÜDü", "KH", "ÜzB", "ÜDa", "ÜzT"])
                    #err.print(["ES", "KS", "DU", "SA", "İY", "ÇA", "ZA", "OL", "ŞA", "KİP", "GÖ", "ÇF", "Kİ", "", "KT", "GE", "SE", "AB", "KBF", "YENİ", "TÜ"])
                    #err.print(["ES", "KS"])

    return errorList
    
    """
    # for parallel data extraction
    #for pair in sentence_pairs:
        #print(pair)
    
    unique_pairs = set(sentence_pairs)

    # Write to a CSV file
    with open("parallel_data_Anna_389_503.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Id", "Original Sentence", "Corrected Sentence"])  # Header
        for id, original, corrected in unique_pairs:
            writer.writerow([id, original, corrected])
    """

def entry_manual_process(errorType, originalText, correctedText):

    err = Error()
    err.idLabelStudio = 1
    err.idData = 1
    err.rawText = originalText
    err.idxStartErr = 0
    err.idxEndErr = len(originalText) # no means
    err.sentOrig = originalText
    err.idxStartSent = 0
    err.idxEndSent = len(originalText) # no means
    err.sentCorr = correctedText
    err.errType = errorType
    err.incorrText = originalText
    err.corrText = correctedText

    err.errTax = Taxonomy()
    err.errTax.pos = POS.mapPOS(err)
    err.errTax.unit = Unit.mapUnit(err)
    err.errTax.phenomenon = Phenomenon.mapPhenomenon(err)
    err.errTax.level = Level.mapLevel(err)
    err.errTax.infFeat = InfFeat.mapInfFeat(err)
    err.errTax.lexFeat = LexFeat.mapLexFeat(err)


    return err






if __name__ == "__main__":
    # to enable running the code with the "path" parameter which is used for Label Studio's json output/export file
    parser = argparse.ArgumentParser(description = "Process a file path.")
    parser.add_argument("path", help = "Path to the Label Studio's json output/export file ")
    
    args = parser.parse_args()
    if globals.debug:
        print(f"Path received: {args.path}")
    
    entry(args.path)
