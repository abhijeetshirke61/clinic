const API_BASE_URL = "http://127.0.0.1:8001";

const form = document.getElementById("booking-form");
const submitBtn = document.getElementById("submit-btn");
const formError = document.getElementById("form-error");

const tableBody = document.getElementById("appt-table-body");
const refreshBtn = document.getElementById("refresh-btn");

function showError(msg) {
    formError.textContent = msg;
}

function clearError() {
    formError.textContent = "";
}

// ---------------- SUBMIT ----------------
form.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearError();

    const payload = {
        patient_name: document.getElementById("patient_name").value,
        mobile_number: document.getElementById("mobile_number").value,
        appointment_date: document.getElementById("appointment_date").value,
        appointment_time: document.getElementById("appointment_time").value
    };

    submitBtn.disabled = true;
    submitBtn.innerText = "Saving...";

    try {
        const res = await fetch(`${API_BASE_URL}/add-patient`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            let bodyText;
            try { bodyText = await res.text(); } catch (e) { bodyText = '<unreadable response>'; }
            throw new Error(`Backend error ${res.status}: ${bodyText}`);
        }

        const data = await res.json();

        alert("Saved Successfully! ID: " + data.patient_id);

        form.reset();
        loadPatients();

    } catch (err) {
           showError("Failed to save data: " + err.message);
           console.error(err);
    }

    submitBtn.disabled = false;
    submitBtn.innerText = "Save & Generate ID";
});

// ---------------- LOAD ----------------
async function loadPatients() {
    tableBody.innerHTML = `<tr><td colspan="6">Loading...</td></tr>`;

    try {
        const res = await fetch(`${API_BASE_URL}/patients`);

        if (!res.ok) throw new Error("API failed");

        const data = await res.json();

        tableBody.innerHTML = data.map(p => `
            <tr>
                <td>${p.id}</td>
                <td>${p.patient_name}</td>
                <td>${p.mobile_number}</td>
                <td>${p.appointment_date}</td>
                <td>${p.appointment_time}</td>
                <td>${p.unique_id}</td>
            </tr>
        `).join("");

    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="6">Failed to load</td></tr>`;
        console.log(err);
    }
}

refreshBtn.addEventListener("click", loadPatients);

loadPatients();