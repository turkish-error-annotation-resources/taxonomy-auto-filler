from enum import Enum

class InfFeat(Enum):
    """ Represents <InflectionalFeature> in the paper https://doi.org/10.1007/s10579-024-09794-0 """

    NONE = 'None'
    GENDER = 'Gender'
    ANIMACY = 'Animacy'
    NOUNCLASS = 'NounClass'
    NUMBER = 'Number'
    CASE = 'Case'
    DEFINITE = 'Definite'
    DEIXIS = 'Deixis'
    DEIXISREF = 'DeixisRef'
    DEGREE = 'Degree'
    VERBFORM = 'VerbForm'
    MOOD = 'Mood'
    TENSE = 'Tense'
    ASPECT = 'Aspect'
    VOICE = 'Voice'
    EVIDENT = 'Evident'
    POLARITY = 'Polarity'
    PERSON = 'Person'
    POLITE = 'Polite'
    CLUSIVITY = 'Clusivity'
    
    @staticmethod
    def mapInfFeat(err):
        return InfFeat.NONE