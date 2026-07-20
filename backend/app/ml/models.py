import joblib
import numpy as np
import logging
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

class DiseaseProgressionModel:
    def __init__(self, model_path="models/disease_progression.joblib"):
        self.model_path = model_path
        self.model = None
        self._load_or_create_model()

    def _load_or_create_model(self):
        try:
            self.model = joblib.load(self.model_path)
            logger.info("Loaded pre-trained disease progression model.")
        except FileNotFoundError:
            logger.warning("No pre-trained model found. Initializing a default RandomForestClassifier.")
            # For demonstration, initialize a dummy model
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            # In a real environment, you would train this model on FHIR/EHR datasets
            # self.model.fit(X_train, y_train)

    def predict_risk(self, patient_features: list[float]) -> float:
        """
        Predict disease progression risk (0.0 to 1.0)
        Features could include age, lab values (e.g. HbA1c), vitals.
        """
        if not hasattr(self.model, "classes_"):
            # Dummy return if model is untrained
            return 0.75 
        
        features_array = np.array(patient_features).reshape(1, -1)
        probabilities = self.model.predict_proba(features_array)
        # Assuming index 1 is the 'high risk' class
        return float(probabilities[0][1])

# Singleton instance for dependency injection
disease_progression_model = DiseaseProgressionModel()
