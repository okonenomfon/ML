document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('creditApplicationForm');
    const resultsModal = new bootstrap.Modal(document.getElementById('resultsModal'));
    const resultsContent = document.getElementById('resultsContent');
    
    const API_URL = 'http://localhost:8000/predict';
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitButton = form.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Processing...';
        
        try {
            const formData = new FormData(form);
            const formDataObj = {};
            
            formData.forEach((value, key) => {
                if (!isNaN(value) && value !== '') {
                    formDataObj[key] = Number(value);
                } else {
                    formDataObj[key] = value;
                }
            });
            
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formDataObj)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const result = await response.json();
            
            displayResults(result);
            resultsModal.show();
            
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your request. Please try again.');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
        }
    });
    
    function displayResults(result) {
        let riskClass = '';
        if (result.risk_status === 'Low Risk') {
            riskClass = 'risk-low';
        } else if (result.risk_status === 'Medium Risk') {
            riskClass = 'risk-medium';
        } else {
            riskClass = 'risk-high';
        }
        
        const probabilityPercentage = (result.risk_probability * 100).toFixed(2);
        
        let html = `
            <div class="risk-result ${riskClass}">
                <h4 class="text-center">${result.risk_status}</h4>
                <p class="text-center mb-0">Application Status: <strong>${result.approval_status}</strong></p>
            </div>
            
            <div class="result-item">
                <div class="result-label">Risk Probability:</div>
                <div>${probabilityPercentage}%</div>
                <div class="probability-bar">
                    <div class="probability-fill bg-${getRiskColor(result.risk_probability)}" 
                         style="width: ${probabilityPercentage}%"></div>
                </div>
            </div>
        `;
        
        if (result.approval_status !== 'Denied') {
            html += `
                <div class="result-item">
                    <div class="result-label">Suggested Interest Rate:</div>
                    <div>${result.suggested_interest_rate}%</div>
                </div>
                
                <div class="result-item">
                    <div class="result-label">Maximum Loan Amount:</div>
                    <div>$${result.max_loan_amount.toLocaleString()}</div>
                </div>
            `;
        }
        
        html += `<div class="mt-3"><strong>Recommendations:</strong><ul>`;
        
        if (result.risk_status === 'High Risk') {
            html += `
                <li>Consider improving your credit score before reapplying</li>
                <li>Reduce your debt-to-income ratio</li>
                <li>Ensure all existing accounts are in good standing</li>
            `;
        } else if (result.risk_status === 'Medium Risk') {
            html += `
                <li>Consider a smaller loan amount</li>
                <li>Provide additional income verification</li>
                <li>A co-signer might improve your terms</li>
            `;
        } else {
            html += `
                <li>You qualify for our best rates</li>
                <li>Consider automatic payments for a 0.25% rate reduction</li>
                <li>You may be eligible for larger loan amounts</li>
            `;
        }
        
        html += `</ul></div>`;
        
        resultsContent.innerHTML = html;
    }
    
    function getRiskColor(probability) {
        if (probability < 0.2) return 'success';
        if (probability < 0.5) return 'warning';
        return 'danger';
    }
});
