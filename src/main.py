import argparse
import globals
from model.error import Error
from model.taxonomy import Taxonomy
from model.level import Level
from model.phenomenon import Phenomenon
from model.unit import Unit
from helper import Helper

def main():
    parser = argparse.ArgumentParser(description = "Process a file path.")
    parser.add_argument("path", help = "Path to the Label Studio's json output/export file ")
    
    args = parser.parse_args()
    print(f"Path received: {args.path}")

    Helper.load_data(args.path)
    Helper.load_abbr_list_TR()

    errorList = []
    for idx, task in enumerate(globals.data): # for each task in input json data
        for result in task["annotations"][0]["result"]: # annotators were informed that they should create only one "annotation" object in Label Studio
            if result["type"] == "labels": # there are two types of results: "labels" (contains error type) and "textarea" (contains corrected form)
                err = Error()
                err.idLabelStudio = task["id"]
                err.idData = task["data"]["ID"]
                err.rawText = task["data"]["DATA"]
                err.idxStartErr = result["value"]["start"]
                err.idxEndErr = result["value"]["end"]
                err.sentOrig, err.idxStartSent, err.idxEndSent = Helper.get_sentence_errored(err.rawText, err.idxStartErr, err.idxEndErr)
                #err.sentCorr = Handler.get_corrected_sentence(data, idx, err.rawText, err.sentOrig, err.sentIdxStart, err.sentIdxEnd)
                err.errType = result["value"]["labels"][0] # from an observational experience, it is known that Label Studio create different result object for the same region that has different label
                err.incorrText = result["value"]["text"]
                err.corrText = Helper.get_corrected_text(idx, result["id"])

                err.errTax = Taxonomy()
                #err.errTax.pos = POS.mapPOS(err.errType, err.incorrText, err.corrText, err.sentOrig)
                #err.errTax.unit = Unit.mapUnit(err.errType, err.incorrText, err.corrText, err.sentOrig) # bazı hata tiplerinde (YA) unit tespiti yapmak gerekiyor
                err.errTax.unit = Unit.mapUnit(err.errType, err.corrText, err.incorrText, err.sentOrig)
                err.errTax.phenomenon = Phenomenon.mapPhenomenon(err.errType, err.corrText, err.incorrText)
                err.errTax.level = Level.mapLevel(err.errType)

                err.print()
                errorList.append(err)
    
if __name__ == "__main__":
    main()