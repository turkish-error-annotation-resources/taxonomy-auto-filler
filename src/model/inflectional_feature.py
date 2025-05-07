from enum import Enum
from helper import Helper
from model.unit import Unit

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

    #todo: is enum type necesssary?

    @staticmethod
    def mapInfFeat(err):
        analysisList = Helper.get_morpholocial_analysis(err)

        resForCorrectedForm = []
        resForErroredMorphemes = []
        for analysis in analysisList:
            infFeatsCorrectedForm = dict(aspect = None, case = None, definite = None, degree = None, evident = None, mood = None, number = None, person = None, polarity = None, tense = None, verbform = None, voice = None, expAttr1_redundantSuffix = None, expAttr2_poss = None)
            infFeats = dict(aspect = None, case = None, definite = None, degree = None, evident = None, mood = None, number = None, person = None, polarity = None, tense = None, verbform = None, voice = None, expAttr1_redundantSuffix = None, expAttr2_poss = None)
            
            analysisPos = str(analysis.getPos())
            analysisFormatLong = str(analysis.formatLong()) # eg. "düşecekti" -> düşmek:Verb] düş:Verb+ecek:Fut+ti:Past+A3sg
            analysisSurfaceForm = str(analysis.surfaceForm()) # eg. "düşecekti"
            
            err.morphAnalysisFormatLong.append(analysisFormatLong) # to be used in lexical feature detection

            # --- --- --- DETECTION FOR CORRECTED FORM --- --- ---
            # Aspect
            if (":Hastily" in analysisFormatLong):
                infFeatsCorrectedForm["aspect"] = "Rap" # Rapid (eg. yapıver, etc.)
            elif any(tag in analysisFormatLong for tag in [":EverSince", ":Repeat"]):
                infFeatsCorrectedForm["aspect"] = "Dur" # Durative (eg. yapagelmiş, yapadurdu etc)
            elif ((":Fut" in analysisFormatLong) and (":Past" in analysisFormatLong)) or (":Almost" in analysisFormatLong):
                infFeatsCorrectedForm["aspect"] = "Prosp" # Prospective (eg. düşecekti, düşeyazdı, etc.)
            elif (":Aor" in analysisFormatLong):
                infFeatsCorrectedForm["aspect"] = "Hab" # Habitual 
            elif (":Prog" in analysisFormatLong):
                infFeatsCorrectedForm["aspect"] = "Prog" # Progressive
            elif any(tag in analysisFormatLong for tag in [":Past", ":Narr", ":Fut"]):
                infFeatsCorrectedForm["aspect"] = "Perf" # Perfect
            elif analysisPos == "Verb":
                infFeatsCorrectedForm["aspect"] = "Imp" # Imperfect (todo: ???)

            # Case
            if (analysisPos == "Noun") and (":Acc" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Acc" # Accusative (Ali'yi, seni, onu, vb.)
            elif (analysisPos == "Noun") and (":Dat" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Dat" # Dative (Ayşe'ye, oraya, buraya, şuna, buna, vb.)
            elif (analysisPos == "Noun") and (":Gen" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Gen" # Genitive (senin, Ali'nin, onun, vb.)
            elif (analysisPos == "Noun") and (":Loc" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Loc" # Locative (sende, bende, şurada, onda, vb.)
            elif (analysisPos == "Noun") and (":Ins" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Ins" # Instrumental (trenle, Ayşe'yle, vb.)
            elif (analysisPos == "Noun") and (":Abl" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Abl" # Ablative (Ali'den, oradan, buradan, vb.)
            elif (analysisPos == "Noun") and (":Equ" in analysisFormatLong):
                infFeatsCorrectedForm["case"] = "Equ" # Equative (bence, sence, vb.)
            else:
                infFeatsCorrectedForm["case"] = "Nom" # Nominative

            # Definite
            # az, bazı, bir, birçok, birkaç, böyle, bu bütün, çoğu, çok, gayri, her
            if analysisPos == "Det":
                if any(tag in analysisSurfaceForm.lower() for tag in ["bu", "şu", "o", "bütün", "her", "aynı", "diğer", "hep", "tüm"]): # bu liste hatalı/eksik/fazla olabilr
                    infFeatsCorrectedForm["definite"] = "Def" # Definite
                elif any(tag in analysisSurfaceForm for tag in ["bir", "bazı", "birkaç", "herhangi", "kimi"]): # bu liste hatalı/eksik/fazla olabilr
                    infFeatsCorrectedForm["definite"] = "Ind" # Indefinite
            else:
                infFeatsCorrectedForm["definite"] = None

            # Degree
            if analysisSurfaceForm == "en":
                infFeatsCorrectedForm["degree"] = "Sup"
            elif analysisSurfaceForm == "daha":
                infFeatsCorrectedForm["degree"] = "Cmp"
            else:
                infFeatsCorrectedForm["degree"] = None

            # Evident
            if analysisPos == "Verb" and "Narr" in analysisFormatLong:
                infFeatsCorrectedForm["evident"] = "Nfh"
            elif analysisPos == "Verb":
                infFeatsCorrectedForm["evident"] = "Fh"
            else:
                infFeatsCorrectedForm["evident"] = None

            # Mood
            if ("+Imp" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "Imp" # Imperative (eg. git, gidin, gitsin, etc.)
            elif (":Opt" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "Opt" # Optative (eg. gidelim, bakayım, etc.)
            elif (":Able" in analysisFormatLong) and (":Neces" in analysisFormatLong) and (":Cop" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "GenNecPot" # General/Hypothetical Necessitative Potential (eg. söyleyebilmelidir, etc.)
            elif (":Neces" in analysisFormatLong) and (":Cop" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "GenNec" # General/Hypothetical Necessitative (eg. kaçmalıdır, etc.)
            elif (":Neces" in analysisFormatLong) and (":Able" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "NecPot" # Necessitative Potential (eg. gidebilmeli, etc.)
            elif (":Neces" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "Nec" # Necessitative (eg. gitmeli, etc.)
            elif (":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "CndGenPot" # Conditional Predicate with Generallized Modality and Potential (eg. gidebilirse, etc.)
            elif (":Unable" in analysisFormatLong) and (":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "GenPotPot" # Generallized Modality and Potential expressed twice (eg. gidemeyebilir)
            elif ((":Unable" in analysisFormatLong) and (":Aor" in analysisFormatLong)) or ((":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong)):
                infFeatsCorrectedForm["mood"] = "GenPot" # General/Hypothetical Potential (eg. yürüyemez, koyabilir, etc.)
            elif (":Unable" in analysisFormatLong) and (":Able" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "PotPot" # Potential expressed twice (eg. gelemeyebileceği, etc.)
            elif (":Aor" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "CndGen" # General Conditional (eg. satarsa, etc.)
            elif (":Able" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "CndPot" # Conditional Potential (eg. çözülebilse, etc.)
            elif (":Cond" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "Cnd" # Conditional (eg. gittiyse, giderse, etc.)
            elif (":Able" in analysisFormatLong) and (":Des" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "DesPot" # Desiderative Potential (eg. yayabilse, etc.)
            elif (":Des" in analysisFormatLong):
                infFeatsCorrectedForm["mood"] = "Des" # Desiderative (eg. uyusa, etc.)
            elif (":Able" in analysisFormatLong): # !!! todo: difference between GenPot !!!
                infFeatsCorrectedForm["mood"] = "Pot" # Potential (eg. gidebilir, koyabilir, etc.)
            elif (":Aor" in analysisFormatLong) or (("Zero→Verb+Pres+A3sg" in analysisFormatLong) and (":Cop" in analysisFormatLong)):
                infFeatsCorrectedForm["mood"] = "Gen" # Generalized Modality (eg. yapılmaz, yürür, eder, hastadır, etc.)
            else:
                infFeatsCorrectedForm["mood"] = "Ind" # Indicative

            # Number (!!! ambiguity with Person !!!)
            if any(tag in analysisFormatLong for tag in ["1pl", "2pl", "3pl"]):
                infFeatsCorrectedForm["number"] = "Plur" # (okuduk, kitaplar, vb.)
            elif any(tag in analysisFormatLong for tag in ["1sg", "2sg", "3sg"]):
                infFeatsCorrectedForm["number"] = "Sing" #(yaptı, kitap, vb.)
            else:
                infFeatsCorrectedForm["number"] = None

            # Person
            if analysisPos == "Verb" or analysisPos == "Pron":
                if any(tag in analysisFormatLong for tag in ["A1pl", "A1sg"]):
                    infFeatsCorrectedForm["person"] = "1st"
                elif any(tag in analysisFormatLong for tag in ["A2pl", "A2sg"]):
                    infFeatsCorrectedForm["person"] = "2nd"
                elif any(tag in analysisFormatLong for tag in ["A3pl", "A3sg"]):
                    infFeatsCorrectedForm["person"] = "3rd"
                else:
                    infFeatsCorrectedForm["person"] = None
            else:
                infFeatsCorrectedForm["person"] = None

            # Polarity
            if analysisPos == "Verb" and "Neg" in analysisFormatLong:
                infFeatsCorrectedForm["polarity"] = "Neg"
            elif analysisPos == "Verb":
                infFeatsCorrectedForm["polarity"] = "Pos"
            else:
                infFeatsCorrectedForm["polarity"] = None

            # Tense
            if (analysisPos == "Verb") and (":Past" in analysisFormatLong) and (":Narr" in analysisFormatLong):
                if (analysisFormatLong.index(":Narr") < analysisFormatLong.index(":Past")):
                    infFeatsCorrectedForm["tense"] = "Pqp" # pluperfect
            elif (analysisPos == "Verb") and analysisFormatLong.count(":Narr") > 1:
                infFeatsCorrectedForm["tense"] = "Pqp" # pluperfect
            elif (analysisPos == "Verb") and any(tag in analysisFormatLong for tag in [":Past", ":Narr"]) :
                infFeatsCorrectedForm["tense"] = "Past" # Past
            elif (analysisPos == "Verb") and (":Fut" in analysisFormatLong):
                infFeatsCorrectedForm["tense"] = "Fut" # Future
            elif (analysisPos == "Verb") and any(tag in analysisFormatLong for tag in [":Prog", ":Aor", "+Pres"]):
                infFeatsCorrectedForm["tense"] = "Pres" # Present
            else:
                infFeatsCorrectedForm["tense"] = None

            # Verbform
            if ("→Adv" in analysisFormatLong):
                infFeatsCorrectedForm["verbform"] = "Conv" # Converb (Verb to Adverb)
            elif ("→Adj" in analysisFormatLong):
                infFeatsCorrectedForm["verbform"] = "Part" # Participle (Verb to Adjactive)
            elif ("→Noun" in analysisFormatLong):
                infFeatsCorrectedForm["verbform"] = "Vnoun" # Verbal Noun (Verb to Noun)
            elif analysisPos == "Verb" and (infFeatsCorrectedForm["mood"] != None or infFeatsCorrectedForm["tense"] != None or infFeatsCorrectedForm["person"] != None):
                infFeatsCorrectedForm["verbform"] = "Fin" # Finite Verb
            else:
                infFeatsCorrectedForm["verbform"] = None

            # Voice
            if (analysisPos == "Verb") and (analysisFormatLong.count(":Caus") > 1) and (":Pass" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "CauCauPass" # Passive Causitive Causitive Voice (e.g. boyattırıldı)
            elif (analysisPos == "Verb") and (":Caus" in analysisFormatLong) and (":Pass" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "CauPassRcp" # Causative Reciprocal Passive Voice (e.g. bölüştürülmedi)
            elif (analysisPos == "Verb") and (":Pass" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "CauPass" # Passive Causative Voice (e.g. boyatıldı)
            elif (analysisPos == "Verb") and (":Caus" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "CauRcp" # Causative Reciprocal Voice (e.g. bölüştürdü)
            elif (analysisPos == "Verb") and (analysisFormatLong.count(":Caus") > 1):
                infFeatsCorrectedForm["voice"] = "CauCau" # Double Causitive Voice (e.g. boyattırdı)
            elif (analysisPos == "Verb") and (":Pass" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "PassRcp" # Combination of Passive and Reciprocal Voices (e.g. paylaşıldı)
            elif (analysisPos == "Verb") and any(tag in analysisFormatLong for tag in ["nıl:Pass", "nil:Pass", "nul:Pass", "nül:Pass"]):
                infFeatsCorrectedForm["voice"] = "PassRfl" # Combination of Passive and Reflexive Voices (e.g. yıkanıldı)
                # todo: This is also Double Pass (PassPass), Because Zemberek do not provide double "Pass" in the "analysisFormatLong", how can it be handled?
            elif (analysisPos == "Verb") and (":Pass" in analysisFormatLong): # n:Pass, ın:Pass, in:Pass, ıl:Pass, il:Pass, ul:Pass, ül:Pass -> Passive Voice (Pass)
                infFeatsCorrectedForm["voice"] = "Pass" # Passive Voice (e.g. boyandı)
            elif (analysisPos == "Verb") and ("Recip" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "Rcp" # Reciprocal Voice (e.g. görüştü)
            elif (analysisPos == "Verb") and (":Caus" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "Cau" # Causitive Voice (e.g. boyattı)
            elif (analysisPos == "Verb") and (":Reflex" in analysisFormatLong):
                infFeatsCorrectedForm["voice"] = "Rfl" # Reflexive Voice (e.g. yıkanmak)
            else:
                infFeatsCorrectedForm["voice"] = None
            
            # Possessiveness (eg. çantam, çantası, çantaları, etc.) -> this is handled in inf_feat instead of lexical because in Turkish possessivness is obtained by inflectional feature
            if (":P1sg" in analysisFormatLong):
                infFeatsCorrectedForm["expAttr2_poss"] = "FirstPersonSingularPossessive"
            elif (":P2sg" in analysisFormatLong):
                infFeatsCorrectedForm["expAttr2_poss"] = "SecondPersonSingularPossessive"
            elif (":P3sg" in analysisFormatLong):
                infFeatsCorrectedForm["expAttr2_poss"] = "ThirdPersonSingularPossessive"
            elif (":P1pl" in analysisFormatLong):
                infFeatsCorrectedForm["expAttr2_poss"] = "FirstPersonPluralPossessive"
            elif (":P2pl" in analysisFormatLong):
                infFeatsCorrectedForm["expAttr2_poss"] = "SecondPersonPluralPossessive"
            elif (":P3pl" in analysisFormatLong):
                infFeatsCorrectedForm["expAttr2_poss"] = "ThirdPersonPluralPossessive"
            else:
                infFeatsCorrectedForm["expAttr2_poss"] = None

            resForCorrectedForm.append(infFeatsCorrectedForm)
            # --- --- --- --- --- --- --- --- --- --- --- --- ---
            
            if (err.errType == 'BA' and err.errTax.unit == Unit.AFFIX) or \
                (err.errType == 'YA' and err.errTax.unit == Unit.AFFIX) or \
                (err.errType == 'ÜzY' and err.errTax.unit == Unit.AFFIX) or \
                (err.errType == 'ÜU') or \
                (err.errType == 'KH') or \
                (err.errType == 'ÜzB'):
                # --- --- --- DETECTION FOR MISTAKEN MORPHEME --- --- ---
                morphemeList = [str(m) for m in analysis.getMorphemes()] # eg. ['Verb:Verb', 'Future:Fut', 'PastTense:Past', 'ThirdPersonSingular:A3sg']
                morphemeSurfaceList = [m.surface for m in analysis.getMorphemeDataList()] # eg. ['düş', 'ecek', 'ti', '']

                # merge morphemeSurfaceList and morphemeList as tuples
                morphemes = []
                for idx, item in enumerate(morphemeSurfaceList):
                    morphemes.append((idx, morphemeSurfaceList[idx], morphemeList[idx]))

                # sometimes zemberek returns empty morpheme surface which corresponds to a morpheme (s.t. A3sg, Verb, etc.)
                # remove these empty morphemes, but keep their indices in emptyMorphemeIdxList because they have corresponding morphemes
                morphemesEmpty = []
                morphemesCleaned = []
                for idx, item in enumerate(morphemes):
                    if item[1] == '':
                        morphemesEmpty.append(item)
                    else:
                        morphemesCleaned.append(item)

                # a simple morpheme alignment approach from left to right which break for the 1st non-match morpheme
                erroredMorphemeList = []
                start = 0
                for idx, item in enumerate(morphemesCleaned):
                    #print(mistakenToken[start:], " --- ", item[1])
                    if not (err.incorrText)[start:].startswith(str(item[1])):
                        erroredMorphemeList.append(item[2])
                        #print("ERROR ON ", item[2])
                        for m in morphemesEmpty:
                            #if m[0] == item[0]+1 and ("A3sg" in m[2]):
                            if m[0] == item[0]+1:
                                erroredMorphemeList.append(m[2])
                                #print("ERROR ON ", m[2])
                        start += len(item[1])
                        break
                    start += len(item[1])

                if len((err.incorrText)[start:]) > 0:
                    erroredMorphemeList.append("REDUNDANT_SUFFIX") # EXPANDED_ATTRUBUTE (if errored text contains the corrected text)

                if len(erroredMorphemeList) > 0:
                    # Aspect
                    if any(":Hastily" in tag for tag in erroredMorphemeList):
                        infFeats["aspect"] = "Rap" # Rapid (eg. yapıver, etc.)
                    elif any(":EverSince" in tag for tag in erroredMorphemeList) or any(":Repeat" in tag for tag in erroredMorphemeList):
                        infFeats["aspect"] = "Dur" # Durative (eg. yapagelmiş, yapadurdu etc)
                    elif (any(":Fut" in tag for tag in erroredMorphemeList) and any(":Past" in tag for tag in erroredMorphemeList)) or any(":Almost" in tag for tag in erroredMorphemeList):
                        infFeats["aspect"] = "Prosp" # Prospective (eg. düşecekti, düşeyazdı, etc.) (todo: this never happen because it is breaked after the first error is detected!)
                    elif any(":Aor" in tag for tag in erroredMorphemeList):
                        infFeats["aspect"] = "Hab" # Habitual
                    elif any(":Prog" in tag for tag in erroredMorphemeList):
                        infFeats["aspect"] = "Prog" # Progressive
                    elif any(":Past" in tag for tag in erroredMorphemeList) or any(":Narr" in tag for tag in erroredMorphemeList) or any(":Fut" in tag for tag in erroredMorphemeList):
                        infFeats["aspect"] = "Perf" # Perfect
                    #elif analysisPos == "Verb":
                        #infFeats["aspect"] = "Imp" # Imperfect (todo: how to be sure if the error is ASPECT:Imp)
                    else:
                        infFeats["aspect"] = None
                    
                    # Case
                    if any(":Acc" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Acc" # Accusative (Ali'yi, seni, onu, vb.)
                    elif any(":Dat" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Dat" # Dative (Ayşe'ye, oraya, buraya, şuna, buna, vb.)
                    elif any(":Gen" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Gen" # Genitive (senin, Ali'nin, onun, vb.)
                    elif any(":Loc" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Loc" # Locative (sende, bende, şurada, onda, vb.)
                    elif any(":Ins" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Ins" # Instrumental (trenle, Ayşe'yle, vb.)
                    elif any(":Abl" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Abl" # Ablative (Ali'den, oradan, buradan, vb.)
                    elif any(":Equ" in tag for tag in erroredMorphemeList):
                        infFeats["case"] = "Equ" # Equative (bence, sence, vb.)
                    #else:
                        #infFeats["case"] = "Nom" # Nominative (todo: how to be sure if the error is CASE:Nom)
                    else:
                        infFeats["case"] = None

                    # Definite
                    # az, bazı, bir, birçok, birkaç, böyle, bu bütün, çoğu, çok, gayri, her
                    # if pos of corrected for is Det; then check for the corrected form surface
                    if analysisPos == "Det":
                        if any(tag in analysisSurfaceForm.lower() for tag in ["bu", "şu", "o", "bütün", "her", "aynı", "diğer", "hep", "tüm"]): # bu liste hatalı/eksik/fazla olabilr
                            infFeats["definite"] = "Def" # Definite
                        elif any(tag in analysisSurfaceForm.lower() for tag in ["bir", "bazı", "birkaç", "herhangi", "kimi"]): # bu liste hatalı/eksik/fazla olabilr
                            infFeats["definite"] = "Ind" # Indefinite
                    else:
                        infFeats["definite"] = None
                    
                    # Degree
                    # check for the corrected form's surface
                    if analysisSurfaceForm == "en":
                        infFeats["degree"] = "Sup"
                    elif analysisSurfaceForm == "daha":
                        infFeats["degree"] = "Cmp"
                    else:
                        infFeats["degree"] = None
                    
                    # Evident
                    if any("Narr" in tag for tag in erroredMorphemeList):
                        infFeats["evident"] = "Nfh"
                    #elif analysisPos == "Verb":
                        #infFeats["evident"] = "Fh" # (todo: how to be sure if the error is EVIDENT:Fh)
                    else:
                        infFeats["evident"] = None
                    
                    # Mood
                    if any(":Imp" in tag for tag in erroredMorphemeList):
                        infFeats["mood"] = "Imp" # Imperative (eg. git, gidin, gitsin, etc.)
                    elif any(":Opt" in tag for tag in erroredMorphemeList):
                        infFeats["mood"] = "Opt" # Optative (eg. gidelim, bakayım, etc.)
                    elif any((":Able" in tag) or (":Neces" in tag) or (":Cop" in tag) for tag in erroredMorphemeList) and (":Able" in analysisFormatLong) and (":Neces" in analysisFormatLong) and (":Cop" in analysisFormatLong):
                        infFeats["mood"] = "GenNecPot" # General/Hypothetical Necessitative Potential (eg. söyleyebilmelidir, etc.)
                    elif any((":Neces" in tag) or (":Cop" in tag) for tag in erroredMorphemeList) and (":Neces" in analysisFormatLong) and (":Cop" in analysisFormatLong):
                        infFeats["mood"] = "GenNec" # General/Hypothetical Necessitative (eg. kaçmalıdır, etc.)
                    elif any((":Neces" in tag) or (":Able" in tag) for tag in erroredMorphemeList) and (":Neces" in analysisFormatLong) and (":Able" in analysisFormatLong):
                        infFeats["mood"] = "NecPot" # Necessitative Potential (eg. gidebilmeli, etc.)
                    elif any(":Neces" in tag for tag in erroredMorphemeList):
                        infFeats["mood"] = "Nec" # Necessitative (eg. gitmeli, etc.)
                    elif any((":Able" in tag) or (":Aor" in tag) or (":Cond" in tag) for tag in erroredMorphemeList) and (":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                        infFeats["mood"] = "CndGenPot" # Conditional Predicate with Generallized Modality and Potential (eg. gidebilirse, etc.)
                    elif any((":Unable" in tag) or (":Able" in tag) or (":Aor" in tag) for tag in erroredMorphemeList) and (":Unable" in analysisFormatLong) and (":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong):
                        infFeats["mood"] = "GenPotPot" # Generallized Modality and Potential expressed twice (eg. gidemeyebilir)
                    elif any((":Unable" in tag) or (":Able" in tag) or (":Aor" in tag) for tag in erroredMorphemeList) and (((":Unable" in analysisFormatLong) and (":Aor" in analysisFormatLong)) or ((":Able" in analysisFormatLong) and (":Aor" in analysisFormatLong))):
                        infFeats["mood"] = "GenPot" # General/Hypothetical Potential (eg. yürüyemez, koyabilir, etc.)
                    elif any((":Unable" in tag) or (":Able" in tag) for tag in erroredMorphemeList) and (":Unable" in analysisFormatLong) and (":Able" in analysisFormatLong):
                        infFeats["mood"] = "PotPot" # Potential expressed twice (eg. gelemeyebileceği, etc.)
                    elif any((":Aor" in tag) or (":Cond" in tag) for tag in erroredMorphemeList) and (":Aor" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                        infFeats["mood"] = "CndGen" # General Conditional (eg. satarsa, etc.)
                    elif any((":Able" in tag) or (":Cond" in tag) for tag in erroredMorphemeList) and (":Able" in analysisFormatLong) and (":Cond" in analysisFormatLong):
                        infFeats["mood"] = "CndPot" # Conditional Potential (eg. çözülebilse, etc.)
                    elif any(":Cond" in tag for tag in erroredMorphemeList):
                        infFeats["mood"] = "Cnd" # Conditional (eg. gittiyse, giderse, etc.)
                    elif any((":Able" in tag) or (":Des" in tag) for tag in erroredMorphemeList) and (":Able" in analysisFormatLong) and (":Des" in analysisFormatLong):
                        infFeats["mood"] = "DesPot" # Desiderative Potential (eg. yayabilse, etc.)
                    elif any(":Des" in tag for tag in erroredMorphemeList):
                        infFeats["mood"] = "Des" # Desiderative (eg. uyusa, etc.)
                    elif any(":Able" in tag for tag in erroredMorphemeList): # !!! todo: difference between GenPot !!!
                        infFeats["mood"] = "Pot" # Potential (eg. gidebilir, koyabilir, etc.)
                    elif any((":Aor" in tag) or (":Cop" in tag) for tag in erroredMorphemeList) and ((":Aor" in analysisFormatLong) or (("Zero→Verb+Pres+A3sg" in analysisFormatLong) and (":Cop" in analysisFormatLong))):
                        infFeats["mood"] = "Gen" # Generalized Modality (eg. yapılmaz, yürür, eder, hastadır, etc.)
                    #else:
                        #infFeats["mood"] = "Ind" # Indicative (todo: how to be sure if the error is MOOD:Ind)
                    else:
                        infFeats["mood"] = None

                    # Number (!!! ambiguity with Person !!!)
                    if any(("1pl" in tag) or ("2pl" in tag) or ("3pl" in tag) for tag in erroredMorphemeList):
                        infFeats["number"] = "Plur" # (okuduk, kitaplar, vb.)
                    elif any(("1sg" in tag) or ("2sg" in tag) or ("3sg" in tag) for tag in erroredMorphemeList):
                        infFeats["number"] = "Sing" #(yaptı, kitap, vb.)
                    else:
                        infFeats["number"] = None
                    
                    # Person
                    if any(("A1pl" in tag) or ("A1sg" in tag) for tag in erroredMorphemeList):
                        infFeats["person"] = "1st"
                    elif any(("A2pl" in tag) or ("A2sg" in tag) for tag in erroredMorphemeList):
                        infFeats["person"] = "2nd"
                    elif any(("A3pl" in tag) or ("A3sg" in tag) for tag in erroredMorphemeList):
                        infFeats["person"] = "3rd"
                    else:
                        infFeats["person"] = None
                    
                    # Polarity
                    if any(":Neg" in tag for tag in erroredMorphemeList):
                        infFeats["polarity"] = "Neg"
                    #elif analysisPos == "Verb":
                        #infFeatsCorrectedForm["polarity"] = "Pos" (todo: how to be sure if the error is POLARITY:Pos)
                    else:
                        infFeats["polarity"] = None

                    # Tense
                    if any((":Narr" in tag) or (":Past" in tag) for tag in erroredMorphemeList) and (":Past" in analysisFormatLong) and (":Narr" in analysisFormatLong):
                        if (analysisFormatLong.index(":Narr") < analysisFormatLong.index(":Past")):
                            infFeats["tense"] = "Pqp" # pluperfect
                    elif any(":Narr" in tag for tag in erroredMorphemeList) and analysisFormatLong.count(":Narr") > 1:
                        infFeats["tense"] = "Pqp" # pluperfect
                    elif any((":Past" in tag) or (":Narr" in tag) for tag in erroredMorphemeList) and any(tag in analysisFormatLong for tag in [":Past", ":Narr"]) :
                        infFeats["tense"] = "Past" # Past
                    elif any(":Fut" in tag for tag in erroredMorphemeList) and (":Fut" in analysisFormatLong):
                        infFeats["tense"] = "Fut" # Future
                    elif any((":Prog" in tag) or (":Aor" in tag) or ("Pres" in tag) for tag in erroredMorphemeList) and any(tag in analysisFormatLong for tag in [":Prog", ":Aor", "+Pres"]):
                        infFeats["tense"] = "Pres" # Present
                    else:
                        infFeats["tense"] = None

                    # Verbform
                    if any(":Adv" in tag for tag in erroredMorphemeList) and ("→Adv" in analysisFormatLong):
                        infFeats["verbform"] = "Conv" # Converb (Verb to Adverb)
                    elif any(":Adj" in tag for tag in erroredMorphemeList) and ("→Adj" in analysisFormatLong):
                        infFeats["verbform"] = "Part" # Participle (Verb to Adjactive)
                    elif any(":Noun" in tag for tag in erroredMorphemeList) and ("→Noun" in analysisFormatLong):
                        infFeats["verbform"] = "Vnoun" # Verbal Noun (Verb to Noun)
                    elif analysisPos == "Verb" and (infFeats["mood"] != None or infFeats["tense"] != None or infFeats["person"] != None):
                        infFeats["verbform"] = "Fin" # Finite Verb
                    else:
                        infFeats["verbform"] = None
                    
                    # Voice
                    if any((":Caus" in tag) or (":Pass" in tag) for tag in erroredMorphemeList) and (analysisFormatLong.count(":Caus") > 1) and (":Pass" in analysisFormatLong):
                        infFeats["voice"] = "CauCauPass" # Passive Causitive Causitive Voice (e.g. boyattırıldı)
                    elif any((":Caus" in tag) or (":Pass" in tag) or (":Recip" in tag) for tag in erroredMorphemeList) and (":Caus" in analysisFormatLong) and (":Pass" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                        infFeats["voice"] = "CauPassRcp" # Causative Reciprocal Passive Voice (e.g. bölüştürülmedi)
                    elif any(":Pass" in tag for tag in erroredMorphemeList) and (":Pass" in analysisFormatLong):
                        infFeats["voice"] = "CauPass" # Passive Causative Voice (e.g. boyatıldı)
                    elif any((":Caus" in tag) or (":Recip" in tag) for tag in erroredMorphemeList) and (":Caus" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                        infFeats["voice"] = "CauRcp" # Causative Reciprocal Voice (e.g. bölüştürdü)
                    elif any(":Caus" in tag for tag in erroredMorphemeList) and (analysisFormatLong.count(":Caus") > 1):
                        infFeats["voice"] = "CauCau" # Double Causitive Voice (e.g. boyattırdı)
                    elif any((":Pass" in tag) or (":Recip" in tag) for tag in erroredMorphemeList) and (":Pass" in analysisFormatLong) and ("Recip" in analysisFormatLong):
                        infFeats["voice"] = "PassRcp" # Combination of Passive and Reciprocal Voices (e.g. paylaşıldı)
                    elif any(":Pass" in tag for tag in erroredMorphemeList) and any(tag in analysisFormatLong for tag in ["nıl:Pass", "nil:Pass", "nul:Pass", "nül:Pass"]):
                        infFeats["voice"] = "PassRfl" # Combination of Passive and Reflexive Voices (e.g. yıkanıldı)
                        # todo: This is also Double Pass (PassPass), Because Zemberek do not provide double "Pass" in the "analysisFormatLong", how can it be handled?
                    elif any(":Pass" in tag for tag in erroredMorphemeList) and (":Pass" in analysisFormatLong): # n:Pass, ın:Pass, in:Pass, ıl:Pass, il:Pass, ul:Pass, ül:Pass -> Passive Voice (Pass)
                        infFeats["voice"] = "Pass" # Passive Voice (e.g. boyandı)
                    elif any(":Recip" in tag for tag in erroredMorphemeList) and ("Recip" in analysisFormatLong):
                        infFeats["voice"] = "Rcp" # Reciprocal Voice (e.g. görüştü)
                    elif any(":Caus" in tag for tag in erroredMorphemeList) and (":Caus" in analysisFormatLong):
                        infFeats["voice"] = "Cau" # Causitive Voice (e.g. boyattı)
                    elif any(":Reflex" in tag for tag in erroredMorphemeList) and (":Reflex" in analysisFormatLong):
                        infFeats["voice"] = "Rfl" # Reflexive Voice (e.g. yıkanmak)
                    else:
                        infFeats["voice"] = None
                    
                    # expAttr1_redundantSuffix
                    if any("REDUNDANT_SUFFIX" in tag for tag in erroredMorphemeList):
                        infFeats["expAttr1_redundantSuffix"] = "True"
                    
                    # Possessiveness (eg. çantam, çantası, çantaları, etc.) -> this is handled in inf_feat instead of lexical because in Turkish possessivness is obtained by inflectional feature
                    if any(":P1sg" in tag for tag in erroredMorphemeList) and (":P1sg" in analysisFormatLong):
                        infFeats["expAttr2_poss"] = "FirstPersonSingularPossessive"
                    elif any(":P2sg" in tag for tag in erroredMorphemeList) and (":P2sg" in analysisFormatLong):
                        infFeats["expAttr2_poss"] = "SecondPersonSingularPossessive"
                    elif any(":P3sg" in tag for tag in erroredMorphemeList) and (":P3sg" in analysisFormatLong):
                        infFeats["expAttr2_poss"] = "ThirdPersonSingularPossessive"
                    elif any(":P1pl" in tag for tag in erroredMorphemeList) and (":P1pl" in analysisFormatLong):
                        infFeats["expAttr2_poss"] = "FirstPersonPluralPossessive"
                    elif any(":P2pl" in tag for tag in erroredMorphemeList) and (":P2pl" in analysisFormatLong):
                        infFeats["expAttr2_poss"] = "SecondPersonPluralPossessive"
                    elif any(":P3pl" in tag for tag in erroredMorphemeList) and (":P3pl" in analysisFormatLong):
                        infFeats["expAttr2_poss"] = "ThirdPersonPluralPossessive"
                    else:
                        infFeats["expAttr2_poss"] = None

                    resForErroredMorphemes.append(infFeats)
                    # --- --- --- --- --- --- --- --- --- --- --- --- ---

        return resForErroredMorphemes