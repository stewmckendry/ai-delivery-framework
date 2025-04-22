class ConcussionValidator:
    def __init__(self):
        self.red_flags = ["loss of consciousness", "vomiting"]

    def validate(self, symptoms):
        return any(symptom in self.red_flags for symptom in symptoms)