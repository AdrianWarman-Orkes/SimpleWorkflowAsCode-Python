class WorkflowInput:
    def __init__(self, email: str, planType: str):
        self.email = email
        self.planType = planType

    def to_dict(self):
        return {
            "email": self.email,
            "planType": self.planType
        }
