document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("prediction-form");
    const errorAlert = document.getElementById("error-alert");

    form.addEventListener("submit", (event) => {
        const floorSize = document.getElementById("floor_size_sq_ft").value;
        const latitude = document.getElementById("latitude").value;
        const longitude = document.getElementById("longitude").value;

        // Validate form inputs
        if (!floorSize || !latitude || !longitude) {
            event.preventDefault(); // Stop form submission
            errorAlert.textContent = "All fields are required!";
            errorAlert.classList.remove("d-none"); // Show the error alert
            return;
        }

        if (isNaN(floorSize) || isNaN(latitude) || isNaN(longitude)) {
            event.preventDefault(); // Stop form submission
            errorAlert.textContent = "Please enter valid numeric values!";
            errorAlert.classList.remove("d-none"); // Show the error alert
            return;
        }

        // Hide error alert if validation passes
        errorAlert.classList.add("d-none");
    });
});

// Function to update displayed range values dynamically
function updateValue(elementId, value) {
    document.getElementById(elementId).textContent = value;
}
