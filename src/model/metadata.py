
# Represents <Taxonomy> in the paper https://doi.org/10.1007/s10579-024-09794-0
class Metadata:
    # constructor
    def __init__(self, taskId=-1, nationality='', gender='', topic=''):
        self.id = taskId
        self.nationality = nationality
        self.gender = gender
        self.topic = topic
    
    def to_dict(self):
        return {
            "id": self.id,
            "nationality": self.nationality,
            "gender": self.gender,
            "topic": self.topic
        }