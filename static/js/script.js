// Selecting form and input elements
const form = document.querySelector("form");
const passwordInput = document.getElementById('password');
const passToggleBtn = document.getElementById('pass-toggle-btn');

// Function to display error messages
const showError = (field, errorText) => {
    field.classList.add("error");
    const errorElement = document.createElement("small");
    errorElement.classList.add("error-text");
    errorElement.innerText = errorText;
    field.closest(".form-group").appendChild(errorElement);
}

// Function to handle form submission
const handleFormData = (e) => {
    e.preventDefault();

    // Retrieving input elements
    const usernameInput = document.getElementById("username");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const dateInput = document.getElementById("date");
    const genderInput = document.getElementById("gender");
    const levelInput = document.getElementById("level");

    // Getting trimmed values from input fields
    const username = usernameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();
    const date = dateInput.value;
    const gender = genderInput.value;
    const level = levelInput.value;

    // Regular expression pattern for email validation
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;

    // Clearing previous error messages
    document.querySelectorAll(".form-group .error").forEach(field => field.classList.remove("error"));
    document.querySelectorAll(".error-text").forEach(errorText => errorText.remove());

    // Performing validation checks
    if (username === "") {
        showError(fullnameInput, "Enter your full name");
    }
    if (!emailPattern.test(email)) {
        showError(emailInput, "Enter a valid email address");
    }
    if (password === "") {
        showError(passwordInput, "Enter your password");
    }
    if (date === "") {
        showError(dateInput, "Select your date of birth");
    }
    if (gender === "") {
        showError(genderInput, "Select your gender");
    }
    if (level === "") {
        showError(genderInput, "Select your gender");
    }

    // Checking for any remaining errors before form submission
    const errorInputs = document.querySelectorAll(".form-group .error");
    if (errorInputs.length > 0) return;

    // Submitting the form
    form.submit();
}

// Toggling password visibility
passToggleBtn.addEventListener('click', () => {
    // Toggle type of password input
    passwordInput.type = passwordInput.type === "password" ? "text" : "password";
    // Toggle class for the icon
    passToggleBtn.className = passwordInput.type === "password" ? "fa-solid fa-eye" : "fa-solid fa-eye-slash";
});


const submitBtn = document.querySelector('.submit-btn input');

submitBtn.addEventListener('click', (e) => {
  e.preventDefault();
  Swal.fire({
    title: 'Pendaftaran Berhasil!',
    text: 'Data Anda telah berhasil disimpan.',
    icon: 'success',
    confirmButtonText: 'OK'
  });
});

// Handling form submission event
form.addEventListener("submit", handleFormData);