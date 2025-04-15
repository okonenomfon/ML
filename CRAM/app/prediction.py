import pickle
import pandas as pd
import numpy as np
from pathlib import Path

MODEL_PATH = Path("models/credit_risk_model.pkl")
FEATURES_PATH = Path("models/required_features.pkl")

def load_model():
    """Load the trained model and required features."""
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    
    with open(FEATURES_PATH, "rb") as f:
        required_features = pickle.load(f)
    
    return model, required_features

model, required_features = load_model()

def predict_credit_risk(application_data):
    """
    Make credit risk prediction based on application data.
    
    Args:
        application_data: Dictionary containing application information
        
    Returns:
        Dictionary with prediction results
    """
    input_df = pd.DataFrame([application_data])
    
    for feature in required_features:
        if feature not in input_df.columns:
            input_df[feature] = np.nan
    
    risk_probability = model.predict_proba(input_df)[0, 1]
    
    if risk_probability < 0.2:
        risk_status = "Low Risk"
        approval_status = "Approved"
        suggested_interest_rate = application_data["interest_rate"]
        max_loan_amount = application_data["loan_amount"] * 1.5
    elif risk_probability < 0.5:
        risk_status = "Medium Risk"
        approval_status = "Conditionally Approved"
        suggested_interest_rate = application_data["interest_rate"] + 2.0
        max_loan_amount = application_data["loan_amount"]
    else:
        risk_status = "High Risk"
        approval_status = "Denied"
        suggested_interest_rate = None
        max_loan_amount = None
    
    return {
        "risk_probability": float(round(risk_probability, 4)),
        "risk_status": risk_status,
        "approval_status": approval_status,
        "suggested_interest_rate": suggested_interest_rate,
        "max_loan_amount": max_loan_amount
    }
