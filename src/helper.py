import config
import json
import requests
import pandas as pd
from model.error_tag import ErrorTag


# Helper class containing static methods for various functionalities
class Helper:
    # loading Label Studio's json output/export file
    @staticmethod
    def load_data(path):
        # loading json file
        try:
            with open(path, 'r') as file:
                config.DATA = json.load(file)

                # ############## TODO:will be deleted (for Elif's re-annotation) ########
                #data_elif = json.load(file)

                # getting task IDs in each sheet by reading Annotations.xlsx file
                #filepath = "./res/Annotations.xlsx"
                #xl = pd.ExcelFile(filepath)
                #sheet_names = xl.sheet_names
                #results = {}
                #for sheet_name in sheet_names:
                    #df = pd.read_excel(filepath, sheet_name=sheet_name, header=None)
                    #results[sheet_name] = df[0].tolist()

                # excluding overlapping tasks in mini-corpus
                #for i in range(len(results["Elif2"])):
                    #for idx, task in enumerate(data_elif):
                        #if results["Elif2"][i] == task["data"]["ID"]:
                            #config.DATA.append(task)
                # ####################################################################

                print("Data is loaded successfully.")
                if config.DEBUG:
                    print(f"Number of tasks in the input file: {len(config.DATA)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}") from e
    
    # validating the loaded data
    @staticmethod
    def validate_data():
        print("Data validation started...")

        # data validation - all spans should be assigned to an error type listed in ErrorTag class
        values = [tag.value for tag in ErrorTag]
        not_assigned_tag_counter = 0
        for idx, task in enumerate(config.DATA):
            for result in task["annotations"][0]["result"]:
                if result["type"] == "labels":
                    if result["value"]["labels"][0] not in values:
                        not_assigned_tag_counter += 1
                        #print(f"DATA_ID: {task["data"]["ID"]}; LABEL: {result["value"]["labels"]}; TEXT: {result["value"]["text"]}; ERROR_ID: {result["id"]}")
        if not_assigned_tag_counter == 0:
            print("Passed. All spans were assigned to valid error types.")
        else:
            print(f"Failed. There are {not_assigned_tag_counter} spans which were not assigned to valid error types.")

        # data validation - the list of annotations for a task should contain only one element
        multi_element_counter = 0
        for task in config.DATA:
            if len(task["annotations"]) > 1:
                multi_element_counter += 1
        if multi_element_counter == 0:
            print("Passed. List of annotations has only one element in each task.")
        else:
            print(f"Failed. There are {multi_element_counter} tasks having more than one element in the list of annotations.")
        
        # data validation - the list of labels for each "labels" type result of a task should contain only one element
        multi_element_counter = 0
        for task in config.DATA:
            for result in task["annotations"][0]["result"]:
                if result["type"] == "labels" and len(result["value"]["labels"]) > 1:
                    multi_element_counter += 1
        if multi_element_counter == 0:
            print("Passed. List of labels has only one element in each labels-type result in each task.")
        else:
            print(f"Failed. There are {multi_element_counter} result object having more than one element in the list of labels.")
        
        # data validation - the list of text for each "textarea" type result of a task should contain only one element
        multi_element_counter = 0
        for task in config.DATA:
            for result in task["annotations"][0]["result"]:
                if result["type"] == "textarea" and len(result["value"]["text"]) > 1:
                    multi_element_counter += 1
        if multi_element_counter == 0:
            print("Passed. List of text has only one element in each textarea-type result in each task.")
        else:
            print(f"Failed. There are {multi_element_counter} result object having more than one element in the list of text.")
        
        # data validation - equal number of labels and textarea type should exist
        isEqual = True
        for task in config.DATA:
            labelsCounter = 0
            textareaCounter = 0
            for result in task["annotations"][0]["result"]:
                if result["type"] == "labels":
                    labelsCounter += 1
                if result['type'] == "textarea":
                    textareaCounter += 1
            if labelsCounter != textareaCounter:
                isEqual = False
                break
        if isEqual:
            print("Passed. Equal number of labels and textarea type exists.")
        else:
            print("Failed. Different number of labels and textarea type exists.")
        
        # data validation - cross overlapping span detection
        cross_span_counter = 0
        for idx, task in enumerate(config.DATA):
            errors_sorted = sorted(config.DATA[idx]["annotations"][0]["result"], key = lambda e: (e["value"]["start"], -e["value"]["end"]))
            
            errors_filtered_by_type = list(filter(lambda x: x["type"] == "labels", errors_sorted))

            seen = set()
            errors_filtered_by_same_span = []
            for x in errors_filtered_by_type:
                key = (x['value']['start'], x['value']['end'])
                if key not in seen:
                    seen.add(key)
                    errors_filtered_by_same_span.append(x)

            for current in errors_filtered_by_same_span:
                cur_start = current['value']['start']
                cur_end = current['value']['end']
                for item in errors_filtered_by_same_span:
                    if item["value"]["start"] < cur_end and item["value"]["start"] > cur_start and item["value"]["end"] > cur_end:
                        cross_span_counter += 1
                        #print(f"DATA_ID: {task["data"]["ID"]};# ERROR_ID: {item['id']};# ERROR_TYPE: {Helper.get_error_type(idx, item['id'])};# TEXT1: {item['value']['text']};# TEXT2: {current['value']['text']}")          
        
        if cross_span_counter == 0:
            print("Passed. Cross-overlap spans not found.")
        else:
            print(f"Failed. Cross-overlap spans found.")

        # data validation - same spans with different labels should have the same corrected text
        same_span_multi_correction_counter = 0
        for idx, task in enumerate(config.DATA):
            for result in task["annotations"][0]["result"]:
                if result["type"] == "labels":
                    startIdx = result["value"]["start"]
                    endIdx = result["value"]["end"]
                    id = result["id"]
                    corrected = Helper.get_corrected_text(idx, id)
                    err_type = result["value"]["labels"][0]
                    dataId = task["data"]["ID"]
                    text = result["value"]["text"]
                    for item in task["annotations"][0]["result"]:
                        if item["type"] == "labels":
                            err_type2 = item["value"]["labels"][0]
                        corr2 = item["value"]["text"][0]
                        if item["type"] == "textarea" and item["id"] != id and item["value"]["start"] == startIdx and item["value"]["end"] == endIdx and corr2 != corrected:
                            same_span_multi_correction_counter += 1
                            #if (err_type != "GEREKSİZ" and err_type2 != "GEREKSİZ"): # TODO: will be deleted!!!
                            #print(f"ID: {dataId}, Text: {text}, Corrected: {corrected}, Corrected2: {corr2}, ErrType: {err_type}, ErrType2: {err_type2}")

        if same_span_multi_correction_counter == 0:
            print("Passed. Same spans with different labels have the same corrected text.")
        else:
            print(f"Failed. Same spans with different labels ({same_span_multi_correction_counter}) should be corrected with the same text.")

        if not_assigned_tag_counter != 0 or multi_element_counter != 0 or isEqual == False or cross_span_counter != 0 or same_span_multi_correction_counter != 0:
            return False
        return True
    
    # loading metadata information for all tasks
    @staticmethod
    def load_metadata():
        try:
            df = pd.read_excel("./res/metadata.xlsx", sheet_name="raw")
            for row in df.values.tolist():
                config.METADATA.append((row[0], str(row[1]).lower(), str(row[2]).lower(), str(row[3]).lower())) # id, nationality, gender, topic
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}") from e

    # loading abbreviations defined by TDK from the abbr_list_tr.xlsx file
    @staticmethod
    def load_abbreviations_tdk():
        try:
            df = pd.read_excel("./res/abbr_list_tr.xlsx")
            for row in df.values.tolist():
                config.ABBREVIATIONS_TDK.append(str(row[0]).lower())
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}") from e
    
    # setting up UDPipe2 REST API call
    @staticmethod
    def setup_udpipe2_call():
        url = f"{config.UDPIPE2_SERVICE}/process"
        payload = {"data": "", # filled when iterating through tasks
                "model": config.UDPIPE2_MODEL, # latest Turkish model (turkish-boun-ud-2.15-241121)
                "tokenizer": "ranges", # used to get token indices
                "input": "horizontal", # input format
                "tagger": "", # model's default
                "parser": "", # model's default
                "output": "conllu" # output format
                }
        return url, payload
    
    # reconstructing the task data by using corrected forms written by annotators
    @staticmethod
    def get_reconstructed_task_data(idx):
        # clear the lookuup list before filling it for the current task
        config.MAP_LOOKUP.clear()

        # sorting errors occured in the task according to the start (asc) and end (desc) index of the error
        errors_sorted = sorted(config.DATA[idx]["annotations"][0]["result"], key = lambda e: (e["value"]["start"], -e["value"]["end"]))

        # only textarea type records are enough to process which contains corrected form
        errors_filtered_by_type = list(filter(lambda x: x["type"] == "textarea", errors_sorted))
        if config.DEBUG:
            print(f"Number of annotations: {len(errors_filtered_by_type)}")

        # for the errors which have the same start and end indices, it is enough to process only one of them becuase annotators wrote the resultant correct form for the same span
        seen = set()
        errors_filtered_by_same_span = []
        for x in errors_filtered_by_type:
            key = (x['value']['start'], x['value']['end'])
            if key not in seen:
                seen.add(key)
                errors_filtered_by_same_span.append(x)
            else:
                # to track how indices change after each correction, format -> (id, start_idx, end_idx, unused, unused)
                config.MAP_LOOKUP.append((x["id"], x["value"]["start"], x["value"]["end"], -1, -1))
        
        # if there are overlapping errors, wider span will be processed, others are removed
        errors_filtered_by_overlapping_span = []
        for current in errors_filtered_by_same_span:
            cur_start = current['value']['start']
            cur_end = current['value']['end']

            # check if current is contained within any already-kept error
            is_contained = False
            overlapped_result_id = -1
            for kept in errors_filtered_by_overlapping_span:
                kept_start = kept['value']['start']
                kept_end = kept['value']['end']

                if kept_start <= cur_start and cur_end <= kept_end:
                    is_contained = True
                    overlapped_result_id = kept["id"]
                    break

            if not is_contained:
                errors_filtered_by_overlapping_span.append(current)
            else:
                # to track how indices change after each correction, format -> (id, start_idx, end_idx, overlapped_result_id, flag="overlap")
                config.MAP_LOOKUP.append((current["id"], current['value']['start'], current["value"]["end"], overlapped_result_id, "overlap"))
        
        # reconstruct the task data by using corrected forms written by annotators
        task_data = config.DATA[idx]["data"]["DATA"]
        offset = 0
        for error in errors_filtered_by_overlapping_span:
            start = error["value"]["start"] + offset
            end = error["value"]["end"] + offset

            task_data = task_data[:start] + error["value"]["text"][0] + task_data[end:]
            offset += len(error["value"]["text"][0]) - (error["value"]["end"] - error["value"]["start"])

            # to track how indices change after each correction, format -> (id, start_idx, end_idx, new_start_idx, new_end_idx)
            config.MAP_LOOKUP.append((error["id"], error["value"]["start"], error["value"]["end"], len(task_data[:start]), len(task_data[:start]) + len(error["value"]["text"][0])))

        config.MAP_LOOKUP = sorted(config.MAP_LOOKUP, key=lambda e: (e[1]))

        return task_data, len(errors_filtered_by_type) # reconstructed task data and number of annotations in the task
    
    # calling UDPipe2 REST API and getting analysis result with conllu format
    @staticmethod
    def call_udpipe_service(reconstructed_task_data, url, payload):
        try:
            payload["data"] = reconstructed_task_data
            response = requests.post(url, data=payload, timeout=(25, 60))
            response.raise_for_status()
            res = response.json()
            
            # UDPipe service sometimes returns error/message instead of result
            if "result" not in res:
                srv_msg = res.get("error") or res.get("message") or "Missing 'result' in UDPipe response."
                raise RuntimeError(f"UDPipe service error: {srv_msg}")
            
            return res["result"]
        
        except requests.exceptions.Timeout as e:
            raise RuntimeError("UDPipe request timed out (connect/read).") from e
        except requests.exceptions.HTTPError as e:
            # include status code and a preview of the response body
            status = e.response.status_code if e.response is not None else "unknown"
            body_preview = (e.response.text[:500].replace("\n", " ") if e.response is not None else "")
            raise RuntimeError(f"UDPipe HTTP error {status}. Body preview: {body_preview}") from e
        except requests.exceptions.RequestException as e:
            # catches connection errors, too many redirects, etc.
            raise RuntimeError(f"UDPipe request failed: {e}") from e
        
    # getting corrected text for a span
    @staticmethod
    def get_corrected_text(idx, result_id):
        for res in config.DATA[idx]["annotations"][0]["result"]:
            if res["id"] == result_id and res["type"] == "textarea":
                return res["value"]["text"][0]

    # getting conllu lines for a given span
    @staticmethod
    def get_conllu_lines_for_span(conllu_text, start_idx, end_idx):
        sentence = ""
        line_list = []
        st_idx = 0
        ed_idx = 0
        multi_token_flag = False
        #print(conllu_text)
        for line in conllu_text.splitlines():
            
            if line.startswith("# text = "):
                sentence = line[len("# text = "):]
                continue

            cols = line.split("\t")
            if len(cols) != 10:
                continue
            
            # according to conllu format
            token_id = cols[0]
            misc = cols[9] # to process TokenRange attribute

            if multi_token_flag:
                if int(token_id) <= ed_idx:
                    line_list.append(line)
                    if int(token_id) == ed_idx:
                        multi_token_flag = False
                else:
                    multi_token_flag = False

            for part in misc.split("|"):
                if part.startswith("TokenRange="):
                    start = int((part.split("=", 1)[1].strip()).split(":", 1)[0].strip())
                    end = int((part.split("=", 1)[1].strip()).split(":", 1)[1].strip())

                    if start_idx <= start and end_idx >= end:
                        line_list.append(line)

                        if "-" in token_id:
                            multi_token_flag = True
                            st_idx, ed_idx = token_id.split("-")
                            st_idx = int(st_idx)
                            ed_idx = int(ed_idx)
                            #print(st_idx, "---", ed_idx)
                    break
        return line_list, sentence

    # finds and returns all punctiation marks in the input text as a list 
    @staticmethod
    def extract_punctuation_marks_TR(text):
        # 17 punctioation marks in Turkish defined by TDK (plus ` and ´)
        punctiation_marks_TR = ['.', ',', ':', ';', '?', '!', '/' '\'', '-', '—', '…', '(', ')', '[', ']', '"', "'", "`", "´" 'ʺ'] 
        return [char for char in text if char in punctiation_marks_TR]