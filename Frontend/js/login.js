document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-form").addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission

        const formData = new FormData(this); // Get the form data

        // Make a POST request to your Flask route using fetch
        fetch("/login", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from your Flask route here
            if (data.success) {
                // Login was successful, redirect or perform necessary actions
                console.log("Login successful:", data.message);
            } else {
                // Login failed, handle the error
                console.error("Login failed:", data.message);
            }
        })
        .catch(error => {
            // Handle network or other errors
            console.error("Error:", error);
        });
    });
});
