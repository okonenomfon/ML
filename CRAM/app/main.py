from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .models import CreditApplication, CreditRiskPrediction
from .prediction import predict_credit_risk
from .config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="API for predicting credit risk based on app data",
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the Credit Risk Assessment API",
        "version": settings.api_version,
        "docs": "/docs",
    }

@app.post("/predict", response_model=CreditRiskPrediction)
async def predict(application: CreditApplication):
    """
    Predict credit risk based on application data.
    
    Returns a risk assessment with probability, status, and recommendations.
    """
    try:
        application_dict = application.dict()
        
        prediction = predict_credit_risk(application_dict)
        
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)
