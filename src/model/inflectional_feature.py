from enum import Enum
from helper import Helper

class InfFeat(Enum):
    """ Represents <InflectionalFeature> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    # not applicable for Turkish
    ANIMACY = 'Animacy'
    CLUSIVITY = 'Clusivity'
    DEIXIS = 'Deixis'
    DEIXISREF = 'DeixisRef'
    GENDER = 'Gender'
    NOUNCLASS = 'NounClass'
    POLITE = 'Polite'
    # applicable for Turkish
    ASPECT = 'Aspect'
    CASE = 'Case'
    DEFINITE = 'Definite'
    DEGREE = 'Degree'
    EVIDENT = 'Evident'
    MOOD = 'Mood'
    NUMBER = 'Number'
    PERSON = 'Person'
    POLARITY = 'Polarity'
    TENSE = 'Tense'
    VERBFORM = 'VerbForm'
    VOICE = 'Voice'

    
    @staticmethod
    def mapInfFeat(err):
        analysisList = Helper.get_morpholocial_analysis(err)

        res = []
        for analysis in analysisList:
            infFeats = dict(aspect = None, case = None, definite = None, degree = None, evident = None, mood = None, number = None, person = None, polarity = None, tense = None, verbform = None, voice = None)
            
            analysisPos = str(analysis.getPos())
            analysisFormatLong = str(analysis.formatLong())
            analysisSurfaceForm = str(analysis.surfaceForm())

            # checking whether the corrected form has following inflectional features
            # Aspect
            if (":Hastily" in analysisFormatLong):
                infFeats["aspect"] = "Rap" # Rapid (eg. yapıver, etc.)
            elif any(tag in analysisFormatLong for tag in [":EverSince", ":Repeat"]):
                infFeats["aspect"] = "Dur" # Durative (eg. yapagelmiş, yapadurdu etc)
            elif ((":Fut" in analysisFormatLong) and (":Past" in analysisFormatLong)) or (":Almost" in analysisFormatLong):
                infFeats["aspect"] = "Prosp" # Prospective (eg. düşecekti, düşeyazdı, etc.)
            elif (":Aor" in analysisFormatLong):
                infFeats["aspect"] = "Hab" # Habitual 
            elif (":Prog" in analysisFormatLong):
                infFeats["aspect"] = "Prog" # Progressive
            elif any(tag in analysisFormatLong for tag in [":Past", ":Narr", ":Fut"]):
                infFeats["aspect"] = "Perf" # Perfect
            elif analysisPos == "Verb":
                infFeats["aspect"] = "Imp" # Imperfect (todo: ???)

            # Case
            if (analysisPos == "Noun") and (":Acc" in analysisFormatLong):
                infFeats["case"] = "Acc" # Accusative (Ali'yi, seni, onu, vb.)
            elif (analysisPos == "Noun") and (":Dat" in analysisFormatLong):
                infFeats["case"] = "Dat" # Dative (Ayşe'ye, oraya, buraya, şuna, buna, vb.)
            elif (analysisPos == "Noun") and (":Gen" in analysisFormatLong):
                infFeats["case"] = "Gen" # Genitive (senin, Ali'nin, onun, vb.)
            elif (analysisPos == "Noun") and (":Loc" in analysisFormatLong):
                infFeats["case"] = "Loc" # Locative (sende, bende, şurada, onda, vb.)
            elif (analysisPos == "Noun") and (":Ins" in analysisFormatLong):
                infFeats["case"] = "Ins" # Instrumental (trenle, Ayşe'yle, vb.)
            elif (analysisPos == "Noun") and (":Abl" in analysisFormatLong):
                infFeats["case"] = "Abl" # Ablative (Ali'den, oradan, buradan, vb.)
            elif (analysisPos == "Noun") and (":Equ" in analysisFormatLong):
                infFeats["case"] = "Equ" # Equative (bence, sence, vb.)
            else:
                infFeats["case"] = "Nom" # Nominative

            # Definite
            # az, bazı, bir, birçok, birkaç, böyle, bu bütün, çoğu, çok, gayri, her
            if analysisPos == "Det":
                if any(tag in analysisSurfaceForm.lower() for tag in ["bu", "şu", "o", "bütün", "her", "aynı", "diğer", "hep", "tüm"]): # bu liste hatalı/eksik/fazla olabilr
                    infFeats["definite"] = "Def" # Definite
                elif any(tag in analysisSurfaceForm for tag in ["bir", "bazı", "birkaç", "herhangi", "kimi"]): # bu liste hatalı/eksik/fazla olabilr
                    infFeats["definite"] = "Ind" # Indefinite
            else:
                infFeats["definite"] = None

            # Degree
            if analysisSurfaceForm == "en":
                infFeats["degree"] = "Sup"
            elif analysisSurfaceForm == "daha":
                infFeats["degree"] = "Cmp"
            else:
                infFeats["degree"] = None

            # Evident
            if analysisPos == "Verb" and "Narr" in analysisFormatLong:
                infFeats["evident"] = "Nfh"
            elif analysisPos == "Verb":
                infFeats["evident"] = "Fh"
            else:
                infFeats["evident"] = None

            # Mood
            if ("+Imp" in analysisFormatLong):
                infFeats["mood"] = "Imp" # Imperative (eg. git, gidin, gitsin, etc.)
            elif (":Opt" in analysisFormatLong):
                infFeats["mood"] = "Opt" # Optative (eg. gidelim, bakayım, etc.)
            elif (":Able" in analysisFormatLong) and (":Neces" in analysisFormatLong) and (":Cop" in analysisFormatLong):
                infFeats["mood"] = "GenNecPot" # General/Hypothetical Necessitative Potential (eg. söyleyebilmelidir, etc.)
            elif (":Neces" in analysisFormatLong) and (":Cop" in analysisFormatLong):
                infFeats["mood"] = "GenNec" # General/Hypothetical Necessitative (eg. kaçmalıdır, etc.)
            elif (":Neces" in analysisFormatLong) and (":Able" in analysisFormatLong):
                infFeats["mood"] = "NecPot" # Necessitative Potential (eg. gidebilmeli, etc.)
            elif (":Neces" in analysisFormatLong):
                infFeats["mood"] = "Nec" # Necessitative (eg. gitmeli, etc.)
            elif (":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                infFeats["mood"] = "CndGenPot" # Conditional Predicate with Generallized Modality and Potential (eg. gidebilirse, etc.)
            elif (":Unable" in analysisFormatLong) and (":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong):
                infFeats["mood"] = "GenPotPot" # Generallized Modality and Potential expressed twice (eg. gidemeyebilir)
            elif ((":Unable" in analysisFormatLong) and (":Aor" in analysisFormatLong)) or ((":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong)):
                infFeats["mood"] = "GenPot" # General/Hypothetical Potential (eg. yürüyemez, koyabilir, etc.)
            elif (":Unable" in analysisFormatLong) and (":Able" in analysisFormatLong):
                infFeats["mood"] = "PotPot" # Potential expressed twice (eg. gelemeyebileceği, etc.)
            elif (":Aor" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                infFeats["mood"] = "CndGen" # General Conditional (eg. satarsa, etc.)
            elif (":Able" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                infFeats["mood"] = "CndPot" # Conditional Potential (eg. çözülebilse, etc.)
            elif (":Cond" in analysisFormatLong):
                infFeats["mood"] = "Cnd" # Conditional (eg. gittiyse, giderse, etc.)
            elif (":Able" in analysisFormatLong) and (":Des" in analysisFormatLong):
                infFeats["mood"] = "DesPot" # Desiderative Potential (eg. yayabilse, etc.)
            elif (":Des" in analysisFormatLong):
                infFeats["mood"] = "Des" # Desiderative (eg. uyusa, etc.)
            elif (":Able" in analysisFormatLong): # !!! todo: difference between GenPot !!!
                infFeats["mood"] = "Pot" # Potential (eg. gidebilir, koyabilir, etc.)
            elif (":Aor" in analysisFormatLong) or (("Zero→Verb+Pres+A3sg" in analysisFormatLong) and (":Cop" in analysisFormatLong)):
                infFeats["mood"] = "Gen" # Generalized Modality (eg. yapılmaz, yürür, eder, hastadır, etc.)
            else:
                infFeats["mood"] = "Ind" # Indicative

            # Number (!!! ambiguity with Person !!!)
            if any(tag in analysisFormatLong for tag in ["1pl", "2pl", "3pl"]):
                infFeats["number"] = "Plur" # (okuduk, kitaplar, vb.)
            elif any(tag in analysisFormatLong for tag in ["1sg", "2sg", "3sg"]):
                infFeats["number"] = "Sing" #(yaptı, kitap, vb.)
            else:
                infFeats["number"] = None

            # Person
            if analysisPos == "Verb" or analysisPos == "Pron":
                if any(tag in analysisFormatLong for tag in ["A1pl", "A1sg"]):
                    infFeats["person"] = "1st"
                elif any(tag in analysisFormatLong for tag in ["A2pl", "A2sg"]):
                    infFeats["person"] = "2nd"
                elif any(tag in analysisFormatLong for tag in ["A3pl", "A3sg"]):
                    infFeats["person"] = "3rd"
                else:
                    infFeats["person"] = None
            else:
                infFeats["person"] = None

            # Polarity
            if analysisPos == "Verb" and "Neg" in analysisFormatLong:
                infFeats["polarity"] = "Neg"
            elif analysisPos == "Verb":
                infFeats["polarity"] = "Pos"
            else:
                infFeats["polarity"] = None

            # Tense
            if (analysisPos == "Verb") and (":Past" in analysisFormatLong) and (":Narr" in analysisFormatLong):
                if (analysisFormatLong.index(":Narr") < analysisFormatLong.index(":Past")):
                    infFeats["tense"] = "Pqp" # pluperfect
            elif (analysisPos == "Verb") and analysisFormatLong.count(":Narr") > 1:
                infFeats["tense"] = "Pqp" # pluperfect
            elif (analysisPos == "Verb") and any(tag in analysisFormatLong for tag in [":Past", ":Narr"]) :
                infFeats["tense"] = "Past" # Past
            elif (analysisPos == "Verb") and (":Fut" in analysisFormatLong):
                infFeats["tense"] = "Fut" # Future
            elif (analysisPos == "Verb") and any(tag in analysisFormatLong for tag in [":Prog", ":Aor", "+Pres"]):
                infFeats["tense"] = "Pres" # Present
            else:
                infFeats["tense"] = "None"

            # Verbform
            if ("→Adv" in analysisFormatLong):
                infFeats["verbform"] = "Conv" # Converb (Verb to Adverb)
            elif ("→Adj" in analysisFormatLong):
                infFeats["verbform"] = "Part" # Participle (Verb to Adjactive)
            elif ("→Noun" in analysisFormatLong):
                infFeats["verbform"] = "Vnoun" # Verbal Noun (Verb to Noun)
            elif analysisPos == "Verb" and (infFeats["mood"] != None or infFeats["tense"] != None or infFeats["person"] != None):
                infFeats["verbform"] = "Fin" # Finite Verb
            else:
                infFeats["verbform"] = None

            # Voice
            if (analysisPos == "Verb") and (analysisFormatLong.count(":Caus") > 1) and (":Pass" in analysisFormatLong):
                infFeats["voice"] = "CauCauPass" # Passive Causitive Causitive Voice (e.g. boyattırıldı)
            elif (analysisPos == "Verb") and (":Caus" in analysisFormatLong) and (":Pass" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                infFeats["voice"] = "CauPassRcp" # Causative Reciprocal Passive Voice (e.g. bölüştürülmedi)
            elif (analysisPos == "Verb") and (":Pass" in analysisFormatLong):
                infFeats["voice"] = "CauPass" # Passive Causative Voice (e.g. boyatıldı)
            elif (analysisPos == "Verb") and (":Caus" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                infFeats["voice"] = "CauRcp" # Causative Reciprocal Voice (e.g. bölüştürdü)
            elif (analysisPos == "Verb") and (analysisFormatLong.count(":Caus") > 1):
                infFeats["voice"] = "CauCau" # Double Causitive Voice (e.g. boyattırdı)
            elif (analysisPos == "Verb") and (":Pass" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                infFeats["voice"] = "PassRcp" # Combination of Passive and Reciprocal Voices (e.g. paylaşıldı)
            elif (analysisPos == "Verb") and any(tag in analysisFormatLong for tag in ["nıl:Pass", "nil:Pass", "nul:Pass", "nül:Pass"]):
                infFeats["voice"] = "PassRfl" # Combination of Passive and Reflexive Voices (e.g. yıkanıldı)
                # todo: This is also Double Pass (PassPass), Because Zemberek do not provide double "Pass" in the "analysisFormatLong", how can it be handled?
            elif (analysisPos == "Verb") and (":Pass" in analysisFormatLong): # n:Pass, ın:Pass, in:Pass, ıl:Pass, il:Pass, ul:Pass, ül:Pass -> Passive Voice (Pass)
                infFeats["voice"] = "Pass" # Passive Voice (e.g. boyandı)
            elif (analysisPos == "Verb") and ("Recip" in analysisFormatLong):
                infFeats["voice"] = "Rcp" # Reciprocal Voice (e.g. görüştü)
            elif (analysisPos == "Verb") and (":Caus" in analysisFormatLong):
                infFeats["voice"] = "Cau" # Causitive Voice (e.g. boyattı)
            elif (analysisPos == "Verb") and (":Reflex" in analysisFormatLong):
                infFeats["voice"] = "Rfl" # Reflexive Voice (e.g. yıkanmak)
            else:
                infFeats["voice"] = None
            
                
            
            res.append(infFeats)
                
        return res