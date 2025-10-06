from enum import Enum

# Represents error tags used in Label Studio
class ErrorTag(Enum):

    # ORTHOGRAPHY
    NO = 'NO' # NOKTALAMA / PUNCTUATION (PUN)
    YA = 'YA' # YAZIM / SPELLING (SPE)
    BA = 'BA' # BİTİŞİK-AYRI / SPACING (SPA)
    BH = 'BH' # BÜYÜK HARF / CAPITALIZATION (CAP)
    Dİ = 'Dİ' # DİYAKRİTİK / DIACRITICS (DIA)
    KI = 'KI' # KISALTMA / ABBREVIATION (ABB)

    # MORPHOPHONOLOGY
    ÜzY = 'ÜzY' # ÜNSÜZ YUMUŞAMASI / CONSONANT VOICING (CV)
    ÜDü = 'ÜDü' # ÜNLÜ DÜŞMESİ / VOWEL DROPPING (VD)
    ÜU = 'ÜU' # ÜNLÜ UYUMU / VOWEL HARMONY (VH)
    KH = 'KH' # KAYNAŞTIRMA HARFİ / BUFFER LETTER (BL)
    ÜzB = 'ÜzB' # ÜNSÜZ BENZEŞMESİ / CONSONANT ASSIMILATION (CA)
    ÜDa = 'ÜDa' # ÜNLÜ DARALMASI / VOWEL NARROWING (VN)
    ÜzT = 'ÜzT' # ÜNSÜZ TÜREMESİ / CONSONANT DOUBLING (CD)

    # GRAMMAR
    SI = 'SI' # SIRA / SEQUENCING (SEQ)
    DU = 'DU' # DURUM / CASE (CASE)
    SA = 'SA' # SAYI / NUMBER (NUM)
    İY = 'İY' # İYELİK / POSSESSION (POSS)
    ÇA = 'ÇA' # ÇATI / VOICE (VOICE)
    ZA = 'ZA' # ZAMAN / TENSE (TENSE)
    KİP = 'KİP' # KİP / MOOD (MOOD)
    GÖ = 'GÖ' # GÖRÜNÜŞ / ASPECT (ASP)
    OL = 'OL' # OLUMSUZLUK / NEGATION (NEG)
    ŞA = 'ŞA' # ŞAHIS / PERSON (PER)
    ÇF = 'ÇF' # ÇEKİMSİZ FİİL / NON-FINITE VERB (NFV)
    SE = 'SE' # SORU EKİ / INTERROGATIVE PARTICLE (IP)
    KK = 'KK' # Kİ KULLANIMI / KI USAGE (KU)
    GE = 'GE' # GEREKSİZ EK / UNNECESSARY AFFIX (UA)
    ST = 'ST' # SÖZCÜK TÜRÜ / LEXICAL CATEGORY (LC)
    TÜ = 'TÜ' # TÜRETME HATASI / DERIVATION (DE)
    AB = 'AB' # ALT BİÇİMBİRİM / ALLOMORPHY (ALL)
    KEG = 'KEG' # KÖK-EK GEÇİŞMESİ / FINAL-INITIAL MERGE (FIM)
    KBF = 'KBF' # KURALLI BİLEŞİK FİİL / DESCRIPTIVE COMPOUND VERB (DCV)

    # OTHERS
    SH = 'SH' # SÖZCÜK HATASI / WORD ERROR (WE)
    İB = 'İB' # İFADE BOZUKLUĞU / AWKWARD PHRASING (AP)
    AnB = 'AnB' # ANLAM BELİRSİZLİĞİ / UNCLEAR MEANING (UM)
    ÜS = 'ÜS' # ÜSLUP / STYLE (STYLE)
    DİJ = 'DİJ' # DİJİTALLEŞTİRME HATASI / DIGITALIZATION ERROR (DE)