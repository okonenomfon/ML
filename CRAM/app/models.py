from pydantic import BaseModel, Field
from typing import Optional

class CreditApplication(BaseModel):
    """
    Pydantic model for credit application input data.
    Adjust these fields based on your model's required features.
    """
    loan_amount: float = Field(..., description="Requested loan amount")
    term: int = Field(..., description="Loan term in months")
    interest_rate: float = Field(..., description="Interest rate")
    installment: float = Field(..., description="Monthly payment amount")
    grade: str = Field(..., description="Loan grade (A-G)")
    employment_length: Optional[float] = Field(None, description="Employment length in years")
    home_ownership: str = Field(..., description="Home ownership status")
    annual_income: float = Field(..., description="Annual income")
    verification_status: str = Field(..., description="Income verification status")
    intent: str = Field(..., description="Loan intent")
    dti: float = Field(..., description="Debt-to-income ratio")
    delinq_2yrs: int = Field(..., description="Number of 30+ days delinquent in past 2 years")
    earliest_credit_line: int = Field(..., description="Year of earliest credit line")
    inq_last_6mths: int = Field(..., description="Inquiries in last 6 months")
    open_accounts: int = Field(..., description="Number of open credit accounts")
    public_records: int = Field(..., description="Number of derogatory public records")
    revolving_balance: float = Field(..., description="Total revolving credit balance")
    revolving_utilization: float = Field(..., description="Revolving line utilization rate")
    total_accounts: int = Field(..., description="Total number of credit accounts")

class CreditRiskPrediction(BaseModel):
    """
    Pydantic model for credit risk prediction output.
    """
    risk_probability: float
    risk_status: str
    approval_status: str
    suggested_interest_rate: Optional[float] = None
    max_loan_amount: Optional[float] = None