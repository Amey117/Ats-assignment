function activateButtonOnFormValidation(formId, buttonId) {
    const form = document.getElementById(formId);
    const button = document.getElementById(buttonId);

    if (!form || !button) {
        console.error("Invalid form ID or button ID.");
        return;
    }

    // Function to check the form's validity
    function checkFormValidity() {
        button.disabled = !form.checkValidity(); // Enable/disable button based on form validity
    }

    // Attach event listeners to all inputs inside the form
    const formElements = form.querySelectorAll("input, select, textarea"); // Includes input, dropdown, textareas
    formElements.forEach((element) => {
        element.addEventListener("input", checkFormValidity); // For text and number inputs
        element.addEventListener("change", checkFormValidity); // For dropdowns and similar fields
    });

    // Initial check to handle pre-filled forms
    checkFormValidity();
}