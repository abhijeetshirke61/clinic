const API_BASE_URL = "http://127.0.0.1:8001";

// ========== ELEMENTS ==========
const authModal = document.getElementById("auth-modal");
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const authStatus = document.getElementById("auth-status");
const logoutBtn = document.getElementById("logout-btn");

const bookingSection = document.getElementById("booking-section");
const bookingsSection = document.getElementById("bookings-section");

const bookingForm = document.getElementById("booking-form");
const submitBtn = document.getElementById("submit-btn");
const formError = document.getElementById("form-error");

const ticket = document.getElementById("ticket");
const ticketPlaceholder = document.getElementById("ticket-placeholder");

const tableBody = document.getElementById("appt-table-body");
const refreshBtn = document.getElementById("refresh-btn");

// ========== STATE ==========
let authToken = localStorage.getItem("authToken") || null;

// ========== AUTH HELPERS ==========
function setToken(token) {
    authToken = token;
    localStorage.setItem("authToken", token);
}

function getToken() {
    return authToken;
}

function clearToken() {
    authToken = null;
    localStorage.removeItem("authToken");
}

function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`
    };
}

// ========== UI STATE MANAGEMENT ==========
function showLoginModal() {
    authModal.style.display = "flex";
    bookingSection.style.display = "none";
    bookingsSection.style.display = "none";
    authStatus.textContent = "Not authenticated";
    logoutBtn.style.display = "none";
}

function showBookingUI() {
    authModal.style.display = "none";
    bookingSection.style.display = "block";
    bookingsSection.style.display = "block";
    authStatus.textContent = "Authenticated ✓";
    logoutBtn.style.display = "inline-block";
}

// ========== LOGIN HANDLER ==========
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    loginError.textContent = "";

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || "Login failed");
        }

        const data = await res.json();
        setToken(data.access_token);
        loginForm.reset();
        showBookingUI();
        loadPatients();

    } catch (err) {
        loginError.textContent = "❌ " + err.message;
        console.error(err);
    }
});

// ========== LOGOUT HANDLER ==========
logoutBtn.addEventListener("click", () => {
    clearToken();
    showLoginModal();
});

// ========== BOOKING FORM HANDLER ==========
bookingForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    formError.textContent = "";

    const payload = {
        patient_name: document.getElementById("patient_name").value,
        mobile_number: document.getElementById("mobile_number").value,
        appointment_date: document.getElementById("appointment_date").value,
        appointment_time: document.getElementById("appointment_time").value,
        notes: document.getElementById("notes").value || ""
    };

    submitBtn.disabled = true;
    submitBtn.textContent = "Saving...";

    try {
        const res = await fetch(`${API_BASE_URL}/add-patient`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            let bodyText = "";
            try {
                const errorData = await res.json();
                bodyText = errorData.detail || JSON.stringify(errorData);
            } catch {
                bodyText = await res.text();
            }
            throw new Error(`${res.status}: ${bodyText}`);
        }

        const data = await res.json();

        // Show confirmation ticket
        displayTicket(data);

        // Reset form and reload list
        bookingForm.reset();
        await loadPatients();

    } catch (err) {
        formError.textContent = "❌ " + err.message;
        console.error(err);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Save & generate ID";
    }
});

// ========== DISPLAY CONFIRMATION TICKET ==========
function displayTicket(patientData) {
    document.getElementById("ticket-name").textContent = patientData.patient_name;
    document.getElementById("ticket-date").textContent = patientData.appointment_date;
    document.getElementById("ticket-time").textContent = patientData.appointment_time;
    document.getElementById("ticket-id").textContent = patientData.patient_id;
    document.getElementById("ticket-status").textContent = patientData.status || "Scheduled";

    ticket.hidden = false;
    ticketPlaceholder.style.display = "none";
}

// ========== LOAD PATIENTS ==========
async function loadPatients() {
    tableBody.innerHTML = `<tr><td colspan="7" class="muted" style="text-align:center; padding:var(--sp-6);">Loading…</td></tr>`;

    try {
        const res = await fetch(`${API_BASE_URL}/patients`, {
            method: "GET",
            headers: getAuthHeaders()
        });

        if (!res.ok) {
            throw new Error(`API failed: ${res.status}`);
        }

        const data = await res.json();

        if (!data || data.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="7" class="muted" style="text-align:center; padding:var(--sp-6);">No appointments yet</td></tr>`;
            return;
        }

        tableBody.innerHTML = data.map(p => `
            <tr>
                <td><strong>${p.patient_id || "—"}</strong></td>
                <td>${p.patient_name || "—"}</td>
                <td>${p.appointment_date || "—"}</td>
                <td>${p.appointment_time || "—"}</td>
                <td>${p.status || "Scheduled"}</td>
                <td>${p.notes || "—"}</td>
                <td style="text-align:center; font-size:0.85rem; color:#999;">${p.unique_id ? p.unique_id.slice(0, 8) : "—"}</td>
            </tr>
        `).join("");

    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="7" class="muted" style="text-align:center; padding:var(--sp-6);">⚠️ ${err.message}</td></tr>`;
        console.error(err);
    }
}

// ========== REFRESH BUTTON ==========
refreshBtn.addEventListener("click", () => {
    if (getToken()) {
        loadPatients();
    }
});

// ========== INITIALIZATION ==========
function init() {
    if (getToken()) {
        showBookingUI();
        loadPatients();
    } else {
        showLoginModal();
    }
}

// Start app
init();