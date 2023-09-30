document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("cita-form").addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent the default form submission

        const formData = {
            nombre_paciente: document.getElementById("nombre_paciente").value,
            email_paciente: document.getElementById("email_paciente").value,
            especialidad: document.getElementById("especialidad").value,
            name_doctor: document.getElementById("name_doctor").value,
            motivo: document.getElementById("motivo").value,
            year: document.getElementById("year").value,
            month: document.getElementById("month").value,
            day: document.getElementById("day").value,
            hour: document.getElementById("hour").value,
            minute: document.getElementById("minute").value
        };

        // Make a POST request to your Flask route using fetch
        fetch("/cita", {
            method: "POST",
            body: JSON.stringify(formData),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response from your Flask route here
            if (data.success) {
                // Consultation scheduled successfully, redirect or perform necessary actions
                console.log("Consultation scheduled:", data.message);
            } else {
                // Consultation scheduling failed, handle the error
                console.error("Consultation scheduling failed:", data.message);
            }
        })
        .catch(error => {
            // Handle network or other errors
            console.error("Error:", error);
        });
    });
});
