const API_BASE_URL = "http://127.0.0.1:8001";

let authToken = null;

// Load token from localStorage on page load
window.addEventListener("load", () => {
    authToken = localStorage.getItem("authToken");
    if (authToken) {
        document.getElementById("auth-section").style.display = "none";
        document.getElementById("booking-form").style.display = "block";
        document.getElementById("patients-section").style.display = "block";
        document.getElementById("logout-btn").style.display = "inline-block";
        loadPatients();
    } else {
        document.getElementById("auth-section").style.display = "block";
        document.getElementById("booking-form").style.display = "none";
        document.getElementById("patients-section").style.display = "none";
        document.getElementById("logout-btn").style.display = "none";
    }
});

// ============== LOGIN ================
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");

if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        loginError.textContent = "";
        
        const username = document.getElementById("login_username").value;
        const password = document.getElementById("login_password").value;
        
        try {
            const res = await fetch(`${API_BASE_URL}/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });
            
            if (!res.ok) {
                let bodyText;
                try { bodyText = await res.text(); } catch (e) { bodyText = '<unreadable>'; }
                throw new Error(`Login failed ${res.status}: ${bodyText}`);
            }
            
            const data = await res.json();
            authToken = data.access_token;
            localStorage.setItem("authToken", authToken);
            
            // Hide login, show booking
            document.getElementById("auth-section").style.display = "none";
            document.getElementById("booking-form").style.display = "block";
            document.getElementById("patients-section").style.display = "block";
            document.getElementById("logout-btn").style.display = "inline-block";
            
            loginForm.reset();
            loadPatients();
            
        } catch (err) {
            loginError.textContent = err.message;
            console.error(err);
        }
    });
}

// ============== LOGOUT ================
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
        authToken = null;
        localStorage.removeItem("authToken");
        document.getElementById("auth-section").style.display = "block";
        document.getElementById("booking-form").style.display = "none";
        document.getElementById("patients-section").style.display = "none";
        document.getElementById("logout-btn").style.display = "none";
    });
}

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

// Helper to add Auth header
function authHeaders() {
    const headers = { "Content-Type": "application/json" };
    if (authToken) {
        headers["Authorization"] = `Bearer ${authToken}`;
    }
    return headers;
}

// ============= SUBMIT ===============
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
            headers: authHeaders(),
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            let bodyText;
            try { bodyText = await res.text(); } catch (e) { bodyText = '<unreadable response>'; }
            throw new Error(`Backend error ${res.status}: ${bodyText}`);
        }

        const data = await res.json();

        // Display confirmation ticket with all appointment details
        document.getElementById("ticket-placeholder").style.display = "none";
        document.getElementById("ticket").style.display = "block";
        document.getElementById("ticket-name").textContent = data.patient_name;
        document.getElementById("ticket-unique-id").textContent = data.unique_id;
        document.getElementById("ticket-date").textContent = data.appointment_date;
        document.getElementById("ticket-time").textContent = data.appointment_time;
        document.getElementById("ticket-id").textContent = data.patient_id;

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

// ============= LOAD ===============
async function loadPatients() {
    tableBody.innerHTML = `<tr><td colspan="6">Loading...</td></tr>`;

    try {
        const res = await fetch(`${API_BASE_URL}/patients`, {
            headers: authHeaders()
        });

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

if (refreshBtn) {
    refreshBtn.addEventListener("click", loadPatients);
}
