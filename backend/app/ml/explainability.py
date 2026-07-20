import shap
import numpy as np
from .models import disease_progression_model

class SHAPExplainer:
    def __init__(self):
        self.explainer = None
        self._initialize_explainer()

    def _initialize_explainer(self):
        # We need a trained model to initialize SHAP TreeExplainer
        # For demonstration purposes, if the model isn't trained, we won't crash
        if hasattr(disease_progression_model.model, "estimators_") and len(disease_progression_model.model.estimators_) > 0:
            self.explainer = shap.TreeExplainer(disease_progression_model.model)

    def explain_prediction(self, patient_features: list[float], feature_names: list[str]) -> dict:
        """
        Generate SHAP values to explain the prediction for a specific patient.
        """
        if not self.explainer:
            return {"error": "Explainer not initialized (model likely untrained)"}

        features_array = np.array(patient_features).reshape(1, -1)
        shap_values = self.explainer.shap_values(features_array)
        
        # Format explanation output for the LangGraph agent and Frontend
        explanation = {}
        # shap_values[1] typically holds the positive class SHAP values for binary classifiers
        values_for_class = shap_values[1] if isinstance(shap_values, list) else shap_values

        for idx, name in enumerate(feature_names):
            explanation[name] = float(values_for_class[0][idx])
            
        return {
            "base_value": float(self.explainer.expected_value[1] if isinstance(self.explainer.expected_value, (list, np.ndarray)) else self.explainer.expected_value),
            "feature_contributions": explanation
        }

shap_explainer = SHAPExplainer()
