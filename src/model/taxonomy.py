from model.pos import POS
from model.unit import Unit
from model.level import Level
from model.phenomenon import Phenomenon
import json

# Represents <Taxonomy> in the paper https://doi.org/10.1007/s10579-024-09794-0
class Taxonomy:
    # constructor
    #def __init__(self, id = '', pos = [], infFeat = [], lexFeat = [], unit = Unit.NONE, phenomenon = Phenomenon.NONE, level = Level.NONE):
    def __init__(self, id = '', pos = [], infFeat = [], lexFeat = [], unit = Unit.NONE, phenomenon = Phenomenon.NONE, level = Level.NONE):
        self.id = id # unique identifier of the error
        self.pos = pos # part-of-speech tag of the error (list structure is used because well-formed utterance may have multiple tokens)
        self.infFeat = infFeat # inflectional feature of the error (list structure is used because well-formed utterance may have multiple tokens)
        self.lexFeat = lexFeat # # lexical feature of the error (list structure is used because well-formed utterance may have multiple tokens)
        self.unit = unit # unit of the error
        self.phenomenon = phenomenon # phenomenon of the error 
        self.level = level # linguistic level of the error
    
    def to_dict(self):
        
        pos_serialized = []
        for item in self.pos:
            form, pos_tag, xpos = item
            pos_serialized.append({
                "form": form,
                "pos": pos_tag,
                "xpos": xpos
            })
        
        infFeat_serialized = []
        for item in self.infFeat:
            form, feats = item
            infFeat_serialized.append({
                "form": form,
                "feats": feats
            })
        
        lexFeat_serialized = []
        for item in self.lexFeat:
            form, feats = item
            lexFeat_serialized.append({
                "form": form,
                "feats": feats
            })
            
        return {
            "id": self.id,
            "pos": pos_serialized,
            "infFeat": infFeat_serialized,
            "lexFeat": lexFeat_serialized,
            "unit": self.unit.value,
            "phenomenon": self.phenomenon.value,
            "level": self.level.value
        }