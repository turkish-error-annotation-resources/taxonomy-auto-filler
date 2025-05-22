from enum import Enum

class Level(Enum):
    """ Represents <Linguistic Level> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    MORPHOPHONOLOGY = 'Morphophonology'
    ORTHOGRAPHY = 'Orthograpy'
    GRAMMAR = 'Grammar'
    SEMANTICS = 'Semantics'
    PRAGMATICS = 'Pragmatics'
    DISCOURSE = 'Discourse'
    SOCIOLINGUISTIC = 'Sociolinguistic'

    def __str__(self):
        return self.value

    @staticmethod
    def mapLevel(err):
        mapping = {
        'HN': Level.ORTHOGRAPHY, # HATALI NOKTALAMA (PUNCTUATION)
        'BA': Level.ORTHOGRAPHY, # BİTİŞİK-AYRI (SPACING)
        'Dİ': Level.ORTHOGRAPHY, # DİYAKRİTİK (DIACTRIC)
        'BH': Level.ORTHOGRAPHY, # BÜYÜK HARF (CAPITALIZATION)
        'KI': Level.ORTHOGRAPHY, # KISALTMA (ABBREVIATION)
        'YA': Level.ORTHOGRAPHY, # YAZIM (SPELLING)
        'ÜzY': Level.MORPHOPHONOLOGY, # ÜNSÜZ YUMUŞAMASI (CONSONANT VOICING)
        'ÜU': Level.MORPHOPHONOLOGY, # ÜNLÜ UYUMU (VOWEL HARMONY)
        'ÜDü': Level.MORPHOPHONOLOGY, # ÜNLÜ DÜŞMESİ (VOWEL DROPPING)
        'KH': Level.MORPHOPHONOLOGY, # KAYNAŞTIRMA HARFİ (BUFFET LETTER)
        'ÜzB': Level.MORPHOPHONOLOGY, # ÜNSÜZ BENZEŞMESİ (CONSONANT ASSIMILIATION)
        'ÜDa': Level.MORPHOPHONOLOGY, # ÜNLÜ DARALMASI (VOWEL NARROWING)
        'ÜzT': Level.MORPHOPHONOLOGY, # ÜNSÜZ TÜREMESİ (CONSONANT DOUBLING)
        'ES': Level.GRAMMAR, # SIRA (SEQUENCING) (TODO: ES - EK SIRASI AND KS - KELİME SIRASI ERRORS WILL BE MERGED AS SI IN LABEL STUDIO)
        'KS': Level.GRAMMAR, # SIRA (SEQUENCING) (TODO: ES - EK SIRASI AND KS - KELİME SIRASI ERRORS WILL BE MERGED AS SI IN LABEL STUDIO)
        'SI':Level.GRAMMAR, # no such label yet
        'DU': Level.GRAMMAR, # DURUM (CASE)
        'SA': Level.GRAMMAR, # SAYI (NUMBER)
        'İY': Level.GRAMMAR, # İYELİK (POSSESSION)
        'ÇA': Level.GRAMMAR, # ÇATI (VOICE)
        'ZA': Level.GRAMMAR, # ZAMAN (TENSE)
        'OL': Level.GRAMMAR, # OLUMSUZLUK (NEGATION)
        'ŞA': Level.GRAMMAR, # ŞAHIS (PERSON)
        'KİP': Level.GRAMMAR, # KİP (MOOD)
        'GÖ': Level.GRAMMAR, # GÖRÜNÜŞ (ASPECT)
        'ÇF': Level.GRAMMAR, # ÇEKİMSİZ FİİL (NON-FINITE VERB)
        'Kİ': Level.GRAMMAR, # Kİ HATASI (KI ERROR)
        'KT': Level.GRAMMAR, # KELİME TÜRÜ (WORD CLASS)
        'GE': Level.GRAMMAR, # GEREKSİZ EK (UNNECESSARY AFFIX)
        'SE': Level.GRAMMAR, # SORU EKİ (INTERROGATIVE PARTICLE)
        'AB': Level.GRAMMAR, # ALT BİÇİMBİRİM (ALLOMORPHY)
        'KBF': Level.GRAMMAR, # KURALLI BİLEŞİK FİİL (DESCRIPTIVE COMPOUND VERB)
        'YENİ': Level.GRAMMAR, # ??? (FINAL-INITIAL MERGE) # TODO: "YENİ" WILL BE CHANGED IN LABEL STUDIO
        'TÜ': Level.GRAMMAR # # TÜRETME (DERIVATIONAL AFFIX)
        }
        
        return mapping.get(err.errType, Level.NONE)