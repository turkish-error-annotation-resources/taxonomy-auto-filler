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
        'ÜzT': Level.MORPHOPHONOLOGY # ÜNSÜZ TÜREMESİ (CONSONANT DOUBLING)
        }
        
        return mapping.get(err.errType, Level.NONE)