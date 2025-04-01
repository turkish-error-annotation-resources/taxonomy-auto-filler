from model.unit import Unit
from model.level import Level
from model.phenomenon import Phenomenon

class Taxonomy:
    """ Represents <Taxonomy> in the paper https://doi.org/10.1007/s10579-024-09794-0  """

    def __init__(self, id = '', pos = [], infFeat = [], lexFeat = [], unit = Unit.NONE, phenomenon = Phenomenon.NONE, level = Level.NONE):
        self.id = id # unique identifier of the error
        self.pos = pos # part-of-speech tag of the error (list structure is used because well-formed utterance may have multiple tokens)
        self.infFeat = infFeat # inflectional feature of the error (list structure is used because well-formed utterance may have multiple tokens)
        self.lexFeat = lexFeat # # lexical feature of the error (list structure is used because well-formed utterance may have multiple tokens)
        self.unit = unit # unit of the error
        self.phenomenon = phenomenon # phenomenon of the error 
        self.level = level # linguistic level of the error