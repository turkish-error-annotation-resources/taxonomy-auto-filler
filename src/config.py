VERSION = "1.0.0"
DEBUG = True
DATA = [] # will hold the input data (Label Studio's json output/export file)
METADATA = [] # used to keep metadata information
ABBREVIATIONS_TDK = [] # used to keep abbreviations defined by TDK
UDPIPE2_SERVICE = "https://lindat.mff.cuni.cz/services/udpipe/api"  # base URL for UDPipe service
UDPIPE2_MODEL = "turkish-boun-ud-2.15-241121" # Turkish model for UDPipe
MAP_LOOKUP = [] # used to find new indices of errors in corrected text