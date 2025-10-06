import argparse
import sys
import config
from model.error import Error
from helper import Helper
from model.taxonomy import Taxonomy
from model.pos import POS
from model.inflectional_feature import InfFeat
from model.lexical_feature import LexFeat
from model.unit import Unit
from model.level import Level
from model.phenomenon import Phenomenon
from model.metadata import Metadata
import json

"""
CONLLU format fields:
ID → Token counter within the sentence (1, 2, 3, …).
FORM → The surface form (exact word in the text).
LEMMA → Dictionary/base form of the word.
UPOS → Universal POS tag (VERB, NOUN, ADJ, etc.).
XPOS → Language-specific part-of-speech tag. ← This is the one you’re asking about.
FEATS → Morphological features (case, tense, number, gender, etc.).
HEAD → ID of the head word (syntactic parent).
DEPREL → Dependency relation to the head (nsubj, obj, root, …).
DEPS → Enhanced dependencies (may contain multiple head:relation pairs).
MISC → Miscellaneous info (e.g., spaces, alignment).
"""

def run(path):
    # loading input file (Label Studio's json output/export file)
    Helper.load_data(path)

    # validating the loaded data (same spans with multiple corrections, cross-overlapping spans, validity of error tags, etc.)
    res_validation = Helper.validate_data()
    if not res_validation:
        print("Data validation failed. Please check the issues above and fix them before running the extender.")
        return []
    
    # loading metadata information for all tasks
    Helper.load_metadata()

    # loading TDK's abbreviation list into globals.abbr_list_TR to be used in Unit detection for error type "NO"/"PUNCTUATION"
    Helper.load_abbreviations_tdk()

    # setting up UDPipe2 REST API call (data of returned payload is empty, it will be loaded later)
    url, payload = Helper.setup_udpipe2_call()

    # main loop through tasks
    print("\nProcessing tasks...")
    errors = []
    for idx, task in enumerate(config.DATA):
        if config.DEBUG:
            print("\n################################################")
            print(f"Task: {idx} --- ID: {task['id']} --- DATA_ID: {task['data']['ID']}")
        
        # task reconstruction
        reconstructed_task_data, no_of_annotations = Helper.get_reconstructed_task_data(idx)
        
        # skip processing the task if lookup table is not matching with the number of annotations
        if no_of_annotations != len(config.MAP_LOOKUP):
            print(f"Number of annotations ({no_of_annotations}) and number of records in MAP_LOOKUP ({len(config.MAP_LOOKUP)}) not matched. Skip processing the task...")
            continue
        
        # UDPipe2 REST API call
        try:
            res_service = Helper.call_udpipe_service(reconstructed_task_data, url, payload)
            #print(res_service)
        except Exception as e:
            print(f"Error occurred while calling UDPipe2 service: {e}")
            continue
        
        # inner loop through results of a task
        for result in task["annotations"][0]["result"]: # annotators were informed that they should create only one "annotation" object in Label Studio (task["annotations"][0] usage is secured because of this assumption)
            if result["type"] == "labels": # there are two types of results: "labels" (contains error type) and "textarea" (contains corrected form)
                err = Error()
                err.id = result["id"] # id of the result
                err.idLabelStudio = task["id"] # id that Label Studio assigned to task (text)
                err.idData = task["data"]["ID"] # id that is coming from the data itself (per text)
                
                # filling out metadata
                res_meta = next((row for row in config.METADATA if row[0] == err.idData), None)
                if res_meta != None:
                    err.metadata = Metadata()
                    err.metadata.id = res_meta[0] # task id
                    err.metadata.nationality = res_meta[1]
                    err.metadata.gender = res_meta[2]
                    err.metadata.topic = res_meta[3]
                
                err.rawText = task["data"]["DATA"] # raw text of task
                err.idxStartErr = result["value"]["start"] # index that the error starts
                err.idxEndErr = result["value"]["end"] # index that the error ends
                err.incorrText = result["value"]["text"] # incorrect text
                err.errType = result["value"]["labels"][0] # type of the error (observational fact; Label Studio creates different result object for the same region which has multiple labels)
                err.corrText = Helper.get_corrected_text(idx, result["id"]) # corrected text of the error span
                
                # taxonomy related features
                err.errTax = Taxonomy()
                
                # variables for case analysis (normal, same-span, overlapping-span)
                start_for_tokenrange = -1
                end_for_tokenrange = -1
                overlap_flag = False

                # if corrected text is empty then pos, infFeat and lexFeat should be None
                if err.corrText.strip() == "":
                    err.errTax.pos = []
                    err.errTax.infFeat = []
                    err.errTax.lexFeat = []
                    #print(f"--- Skipped Error {err.idData, err.errType} ---")
                # if corrected text is not empty then pos, infFeat and lexFeat should be assigned
                else:
                    # finding the record in MAP_LOOKUP for current error id
                    err_in_lookup = next((q for q in config.MAP_LOOKUP if q[0] == err.id), None)
                    # same span case -> MAP_LOOKUP structure: (result_id, start_idx, end_idx, -1, -1)
                    if err_in_lookup[3] == -1 and err_in_lookup[4] == -1:
                        # finding record in MAP_LOOKUP for this span which is not -1 in its 3rd and 4th positions, it will be either normal or overlapped
                        alt_err = next((r for r in config.MAP_LOOKUP if r[1] == err_in_lookup[1] and r[2] == err_in_lookup[2] and r[2] != -1 and r[3] != -1), None)
                        if alt_err[4] == "overlap": # if it is overlap
                            overlap_err = next((o for o in config.MAP_LOOKUP if o[0] == alt_err[3]), None)
                            start_for_tokenrange = overlap_err[3]
                            end_for_tokenrange = overlap_err[4]
                            overlap_flag = True
                        else: # if it is normal
                            start_for_tokenrange = alt_err[3]
                            end_for_tokenrange = alt_err[4]
                    
                    # overlapping span case  -> MAP_LOOKUP structure: (result_id, start_idx, end_idx, overlapping_err_result_id, "overlap")
                    # important: always the same biggest span is refered for nested overlapping spans
                    elif err_in_lookup[4] == "overlap":
                        overlap_err = next((o for o in config.MAP_LOOKUP if o[0] == err_in_lookup[3]), None)
                        start_for_tokenrange = overlap_err[3]
                        end_for_tokenrange = overlap_err[4]
                        overlap_flag = True

                    # normal case -> MAP_LOOKUP structure: (result_id, start_idx, end_idx, start_idx_for_tokenrange, end_idx_for_tokenrange)
                    else:
                        start_for_tokenrange = err_in_lookup[3]
                        end_for_tokenrange = err_in_lookup[4]
                
                # getting conllu lines from udpipe2 api call result which are related to the error (selected span)
                line_list, sentence = Helper.get_conllu_lines_for_span(res_service, start_for_tokenrange, end_for_tokenrange)

                err.errTax.id = err.id
                err.errTax.pos = POS.mapPOS(err, line_list, overlap_flag)
                err.errTax.infFeat = InfFeat.mapInfFeat(err, line_list, overlap_flag)
                err.errTax.lexFeat = LexFeat.mapLexFeat(err, line_list, overlap_flag)
                err.errTax.unit = Unit.mapUnit(err, line_list, overlap_flag, sentence)
                err.errTax.phenomenon = Phenomenon.mapPhenomenon(err, line_list, overlap_flag)
                err.errTax.level = Level.mapLevel(err)


                print("\n##########################")
                #for item in line_list:
                #    print(item)
                print(f"Error ID: {err.errTax.id}")
                print(f"Corrected Text: {err.corrText}")
                print(f"POS: {err.errTax.pos}")
                print(f"Inflectional Features: {err.errTax.infFeat}")
                print(f"Lexical Features: {err.errTax.lexFeat}")
                print(f"Unit: {err.errTax.unit.value}")
                print(f"Phenomenon: {err.errTax.phenomenon.value}")
                print(f"Level: {err.errTax.level.value}")
                print(f"Nationality: {err.metadata.nationality}")
                print(f"Gender: {err.metadata.gender}")
                print(f"Topic: {err.metadata.topic}")

                errors.append(err)

    return errors


# run the extender with the following command: python src/main.py "/Users/tolgahanturker/Downloads/***.json"
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semi-automated Annotation Extender")
    parser.add_argument("path", help="File path to the exported JSON annotations from Label Studio.")
    
    if len(sys.argv) == 1:
        print("Missing required argument 'path'.\n", file=sys.stderr)
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    if config.DEBUG:
        print(f"Input File Path: {args.path}")
    
    enriched_errors = run(args.path)

    # TODO: will be deleted
    #errors_as_dicts = [e.to_dict() for e in enriched_errors]
    #with open("./res/errors_elif.json", "w", encoding="utf-8") as f:
        #json.dump(errors_as_dicts, f, ensure_ascii=False, indent=4)