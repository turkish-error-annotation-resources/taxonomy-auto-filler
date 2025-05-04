from enum import Enum

class Level(Enum):
    """ Represents <Linguistic Level> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 0
    MORPHOPHONOLOGY = 1
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
        'ÜzY': Level.MORPHOPHONOLOGY, # ÜNSÜZ YUMUŞAMASI (CONSONANT VOICING)
        'ÜU': Level.MORPHOPHONOLOGY, # ÜNLÜ UYUMU (VOWEL HARMONY)
        'ÜDü': Level.MORPHOPHONOLOGY, # ÜNLÜ DÜŞMESİ (VOWEL DROPPING)
        'KH': Level.MORPHOPHONOLOGY, # KAYNAŞTIRMA HARFİ (BUFFET LETTER)
        'ÜzB': Level.MORPHOPHONOLOGY, # ÜNSÜZ BENZEŞMESİ (CONSONANT ASSIMILIATION)
        'ÜDa': Level.MORPHOPHONOLOGY, # ÜNLÜ DARALMASI (VOWEL NARROWING)
        'ÜT': Level.MORPHOPHONOLOGY, # ÜNLÜ TÜREMESİ (?)
        'ÜzT': Level.MORPHOPHONOLOGY # ÜNSÜZ TÜREMESİ (CONSONANT DOUBLING)
        }
        
        return mapping.get(errType, Level.NONE)