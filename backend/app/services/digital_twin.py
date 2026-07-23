import copy

class HealthcareDigitalTwin:
    """
    Simulates patient profiles for 'What-If' clinical trial eligibility analysis.
    Doctors can adjust a patient's lab values or medications to see if they 
    would qualify for a trial under different conditions.
    """
    def __init__(self, base_patient_profile: dict):
        self.base_profile = copy.deepcopy(base_patient_profile)
        self.simulated_profile = copy.deepcopy(base_patient_profile)

    def adjust_lab_value(self, loinc_code: str, new_value: float):
        """Adjust a specific lab observation (e.g. HbA1c)."""
        if "observations" not in self.simulated_profile:
            self.simulated_profile["observations"] = {}
        self.simulated_profile["observations"][loinc_code] = new_value
        return self

    def adjust_medication(self, rxnorm_code: str, action: str):
        """Add or remove a medication from the simulated profile."""
        if "medications" not in self.simulated_profile:
            self.simulated_profile["medications"] = []
            
        if action == "add":
            if rxnorm_code not in self.simulated_profile["medications"]:
                self.simulated_profile["medications"].append(rxnorm_code)
        elif action == "remove":
            if rxnorm_code in self.simulated_profile["medications"]:
                self.simulated_profile["medications"].remove(rxnorm_code)
        return self
        
    def get_profile(self):
        return self.simulated_profile
