from enum import Enum

class Level(Enum):
    """ Represents <Linguistic Level> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 0
    PHONOLOGY = 1
    ORTHOGRAPHY = 2
    GRAMMAR = 3
    SEMANTICS = 4
    PRAGMATICS = 5
    DISCOURSE = 6
    SOCIOLINGUISTIC = 7

    @staticmethod
    def mapLevel(errType):
        mapping = {
        'HN': Level.ORTHOGRAPHY, # HATALI NOKTALAMA (PUNCTUATION)
        'BA': Level.ORTHOGRAPHY, # BİTİŞİK-AYRI (SPACING)
        'Dİ': Level.ORTHOGRAPHY, # DİYAKRİTİK (DIACTRIC)
        'BH': Level.ORTHOGRAPHY, # BÜYÜK HARF (CAPITALIZATION)
        'KI': Level.ORTHOGRAPHY, # KISALTMA (ABBREVIATION)
        'YA': Level.ORTHOGRAPHY, # YAZIM (SPELLING)
        'ÜzY': Level.PHONOLOGY, # ÜNSÜZ YUMUŞAMASI (CONSONANT VOICING)
        'ÜU': Level.PHONOLOGY, # ÜNLÜ UYUMU (VOWEL HARMONY)
        'ÜDü': Level.PHONOLOGY, # ÜNLÜ DÜŞMESİ (VOWEL DROPPING)
        'KH': Level.PHONOLOGY, # KAYNAŞTIRMA HARFİ (BUFFET LETTER)
        'ÜzB': Level.PHONOLOGY, # ÜNSÜZ BENZEŞMESİ (CONSONANT ASSIMILIATION)
        'ÜDa': Level.PHONOLOGY, # ÜNLÜ DARALMASI (VOWEL NARROWING)
        'ÜT': Level.PHONOLOGY, # ÜNLÜ TÜREMESİ (?)
        'ÜzT': Level.PHONOLOGY # ÜNSÜZ TÜREMESİ (CONSONANT DOUBLING)
        }
        
        return mapping.get(errType, Level.NONE)