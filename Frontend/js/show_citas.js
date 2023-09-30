var citasContainer = document.getElementById("citas-container");
var currentRow = null;

// Sample JSON array of citas
var sampleCitas = [
    {
        "id": "1",
        "nombre_paciente": "John Doe",
        "motivo": "Regular checkup"
    },
    {
        "id": "2",
        "nombre_paciente": "Alice Smith",
        "motivo": "Dental appointment"
    },
    {
        "id": "3",
        "nombre_paciente": "Bob Johnson",
        "motivo": "Follow-up consultation"
    },
    // Add more sample cita objects as needed
];

function createCitas() {
    citasContainer.innerHTML = "";

    // You can use the sampleCitas array instead of making an HTTP request
    var citas = sampleCitas;

    // Generate the citas in the frontend
    for (var i = 0; i < citas.length; i++) {
        (function () {
            var cita = citas[i];
            var citaCard = document.createElement("div");
            citaCard.className = "col-md-4 ftco-animate fadeInUp ftco-animated";

            var blogEntry = document.createElement("div");
            blogEntry.className = "blog-entry";

            // Add the background image here if needed
            var block20 = document.createElement("a");
            block20.href = "blog-single.html"; // Replace with the actual link
            block20.className = "block-20";
            block20.style.backgroundImage = "url('images/image_1.jpg')";

            blogEntry.appendChild(block20);

            var textBlock = document.createElement("div");
            textBlock.className = "text d-block";

            var metaDiv = document.createElement("div");
            metaDiv.className = "meta mb-3";

            var metaDate = document.createElement("div");
            var dateLink = document.createElement("a");
            dateLink.href = "#"; // Replace with the actual link
            dateLink.textContent = "June 9, 2019";
            metaDate.appendChild(dateLink);
            metaDiv.appendChild(metaDate);

            var metaAdmin = document.createElement("div");
            var adminLink = document.createElement("a");
            adminLink.href = "#"; // Replace with the actual link
            adminLink.textContent = "Admin";
            metaAdmin.appendChild(adminLink);
            metaDiv.appendChild(metaAdmin);

            var metaChat = document.createElement("div");
            var chatLink = document.createElement("a");
            chatLink.href = "#"; // Replace with the actual link
            chatLink.className = "meta-chat";
            var chatIcon = document.createElement("span");
            chatIcon.className = "icon-chat";
            chatLink.appendChild(chatIcon);
            chatLink.textContent = " 3";
            metaChat.appendChild(chatLink);
            metaDiv.appendChild(metaChat);

            textBlock.appendChild(metaDiv);

            var citaHeading = document.createElement("h3");
            var headingLink = document.createElement("a");
            headingLink.href = "blog-single.html"; // Replace with the actual link
            headingLink.textContent = cita.nombre_paciente;
            citaHeading.className = "heading";
            citaHeading.appendChild(headingLink);
            textBlock.appendChild(citaHeading);

            var citaMotivo = document.createElement("p");
            citaMotivo.textContent = cita.motivo;
            textBlock.appendChild(citaMotivo);

            var prescriptionButton = document.createElement("button");
            prescriptionButton.className = "btn btn-primary py-2 px-3";
            prescriptionButton.textContent = "Prescription";
            // Use data-* attribute to store cita information
            prescriptionButton.setAttribute("data-cita-id", cita.id);
            prescriptionButton.addEventListener("click", function () {
                openPrescriptionForm(this.getAttribute("data-cita-id")); // Pass cita ID
            });
            
            textBlock.appendChild(prescriptionButton);

            blogEntry.appendChild(textBlock);
            citaCard.appendChild(blogEntry);

            if (i % 3 == 0) {
                currentRow = document.createElement("div");
                currentRow.className = "row";
                citasContainer.appendChild(currentRow);
            }

            // Remove the column element and append the citaCard directly to the currentRow
            // Alternatively, keep the column element but remove the col-md-4 class from the citaCard
            currentRow.appendChild(citaCard);
        })();
    }
}

// Function to open the prescription form
// Function to open the prescription form
function openPrescriptionForm(citaId) {
    var cita = getCitaById(citaId);

    if (cita) {
        // Create a Bootstrap modal
        var modal = document.createElement("div");
        modal.className = "modal fade";
        modal.tabIndex = -1;
        modal.setAttribute("role", "dialog");

        var modalDialog = document.createElement("div");
        modalDialog.className = "modal-dialog";
        modalDialog.setAttribute("role", "document");

        var modalContent = document.createElement("div");
        modalContent.className = "modal-content";

        var modalHeader = document.createElement("div");
        modalHeader.className = "modal-header";
        modalHeader.innerHTML = "<h5 class='modal-title'>Prescription Form</h5><button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button>";

        var modalBody = document.createElement("div");
        modalBody.className = "modal-body";

        // Create form inputs for medicines and prescription
        var medicinesFormGroup = document.createElement("div");
        medicinesFormGroup.className = "form-group";
        medicinesFormGroup.innerHTML = "<label for='medicines'>Medicines:</label><input type='text' class='form-control' id='medicines' placeholder='Enter medicines here'>";

        var prescriptionFormGroup = document.createElement("div");
        prescriptionFormGroup.className = "form-group";
        prescriptionFormGroup.innerHTML = "<label for='prescription'>Prescription:</label><textarea class='form-control' id='prescription' rows='4' placeholder='Enter prescription here'></textarea>";

        modalBody.appendChild(medicinesFormGroup);
        modalBody.appendChild(prescriptionFormGroup);

        var modalFooter = document.createElement("div");
        modalFooter.className = "modal-footer";
        var submitButton = document.createElement("button");
        submitButton.type = "button";
        submitButton.className = "btn btn-primary";
        submitButton.textContent = "Submit";
        submitButton.addEventListener("click", function () {
            var medicines = document.getElementById("medicines").value;
            var prescription = document.getElementById("prescription").value;
        
            // Create an object with the form data
            var formData = {
                indicaciones: medicines,
                medicamentos: prescription,
                id_cita: citaId
            };
        
            // Send the form data to the /receta route using fetch
            fetch("/receta", {
                method: "POST",
                body: JSON.stringify(formData),
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Prescription was successfully created
                    console.log("Prescription created:", data.message);
                    // Handle any further actions (e.g., display success message)
                } else {
                    // Handle the case where prescription creation failed
                    console.error("Prescription creation failed:", data.message);
                    // Display an error message or take appropriate action
                }
                closeModal(); // Close the modal after handling the response
            })
            .catch(error => {
                console.error("Error sending prescription data:", error);
                // Handle the error (e.g., display an error message)
                closeModal(); // Close the modal in case of an error
            });
        });
        modalFooter.appendChild(submitButton);

        modalContent.appendChild(modalHeader);
        modalContent.appendChild(modalBody);
        modalContent.appendChild(modalFooter);

        modalDialog.appendChild(modalContent);
        modal.appendChild(modalDialog);

        // Display the Bootstrap modal
        $(modal).modal();

        // Remove the modal from the DOM when closed
        $(modal).on("hidden.bs.modal", function () {
            modal.remove();
        });
    }
}


// Function to close the modal
function closeModal() {
    var modal = document.querySelector(".modal");
    if (modal) {
        modal.remove();
    }
}

// Function to retrieve cita by ID from the sampleCitas array
function getCitaById(citaId) {
    return sampleCitas.find(function (cita) {
        return cita.id === citaId;
    });
}

// ...



// Call the function to create citas using the sample data
createCitas();
