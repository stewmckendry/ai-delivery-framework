class ConcussionAgent:
    def __init__(self):
        self.symptoms = []
        self.stage = "initial"

    def parse_input(self, text):
        if "headache" in text:
            self.symptoms.append("headache")
        if "dizzy" in text:
            self.symptoms.append("dizziness")

    def advance_stage(self):
        if self.stage == "initial":
            self.stage = "monitoring"
        elif self.stage == "monitoring":
            self.stage = "cleared"
        return self.stage

    def is_clear(self):
        return self.stage == "cleared"