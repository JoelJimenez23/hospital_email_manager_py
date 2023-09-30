// app.js

document.addEventListener("DOMContentLoaded", function () {
    // Fetch specialties from the server and populate the select options
    var especialidadSelect = document.getElementById("especialidad");

    fetch("/specialties")
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                data.specialties.forEach(function (specialty) {
                    var option = document.createElement("option");
                    option.text = specialty;
                    especialidadSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error("Error fetching specialties:", error);
        });

    // When the specialty is selected, fetch doctors for that specialty and populate the select options
    var nameDoctorSelect = document.getElementById("name_doctor");
    especialidadSelect.addEventListener("change", function () {
        var selectedSpecialty = this.value;
        nameDoctorSelect.innerHTML = ""; // Clear existing options

        fetch("/doctors?especialidad=" + selectedSpecialty)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    data.doctors.forEach(function (doctor) {
                        var option = document.createElement("option");
                        option.text = doctor;
                        nameDoctorSelect.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error("Error fetching doctors:", error);
            });
    });
});
