# CareLine Clinic - Deployment Guide

## Project Status: ✅ READY FOR DEPLOYMENT

All endpoints tested and working. Backend and Frontend fully functional with JWT authentication.

---

## Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js (if using live-server)
- Internet connection (for Supabase)

### 1. Start Backend (FastAPI)

```bash
cd BAACK
python -m uvicorn main:app --reload --port 8001
```

**Backend URL:** http://127.0.0.1:8001

Available endpoints:
- `POST /login` - User authentication
- `POST /add-patient` - Create appointment (requires JWT)
- `GET /patients` - Get all appointments (requires JWT)
- `GET /ping` - Health check
- `GET /docs` - Swagger UI documentation

---

### 2. Start Frontend (HTML/JS)

Option A: Using Live Server (VSCode Extension)
```bash
# Open FRONT/index.html and right-click → "Open with Live Server"
# Or
cd FRONT
npx http-server -p 5500
```

Option B: Python's built-in server
```bash
cd FRONT
python -m http.server 5500
```

**Frontend URL:** http://127.0.0.1:5500

---

## API Documentation

### Swagger UI (Interactive Testing)
- **URL:** http://127.0.0.1:8001/docs
- **Features:** Try endpoints directly from browser, auto-generated from code

### ReDoc (Alternative View)
- **URL:** http://127.0.0.1:8001/redoc

---

## User Authentication

**Demo Credentials:**
- Username: `admin`
- Password: `password`

### JWT Flow
1. Login: `POST /login` with credentials
2. Get token from response
3. Use token in `Authorization: Bearer <token>` header for protected endpoints

---

## Database

**Supabase Connection:**
- Table: `patients`
- Automatically generates:
  - `patient_id` (PAT001, PAT002, etc.)
  - `unique_id` (UUID for tracking)
  - `status` (default: scheduled)
  - `created_at` (timestamp)

---

## Project Structure

```
QUICK CLINIC/
├── BAACK/                 # Backend
│   ├── main.py           # FastAPI app (5 endpoints)
│   ├── database.py       # Supabase config
│   ├── test_auth.py      # JWT auth test
│   └── test_deployment.py # Full flow test
│
└── FRONT/                # Frontend
    ├── index.html        # Login form + booking form
    ├── script-jwt.js     # JWT auth + API calls
    ├── style.css         # UI styling
    └── README.md         # (You can create this)
```

---

## Features Implemented

✅ **Authentication**
- JWT token-based auth
- Demo admin credentials
- 60-minute token expiry

✅ **Appointments**
- Create new patient appointments
- Auto-generate patient IDs
- View all appointments
- Track with unique IDs

✅ **API Documentation**
- Swagger UI with interactive testing
- Full parameter documentation
- Response examples

✅ **Security**
- CORS configured for local development
- JWT bearer token validation
- HTTPException error handling

✅ **Database**
- Supabase integration
- Persistent patient records

---

## Testing Checklist

Run these commands to verify deployment:

```bash
# Test full flow
cd BAACK
python test_deployment.py

# Should see:
# ✓ LOGIN SUCCESSFUL
# ✓ PATIENT CREATED SUCCESSFULLY
# ✓ PATIENTS RETRIEVED SUCCESSFULLY
# ✓ PING ENDPOINT WORKING
# ✅ ALL TESTS PASSED
```

---

## Troubleshooting

### Backend not starting
```bash
# Check port 8001 is free
netstat -an | findstr 8001

# Kill existing process on port 8001 (Windows)
taskkill /PID <process_id> /F
```

### CORS errors
- Already configured in `main.py` for local development
- Allows requests from `http://127.0.0.1:5500`

### JWT token expired
- Tokens expire after 60 minutes
- Get new token by logging in again at `/login`

### Frontend can't reach backend
- Verify backend is running on `http://127.0.0.1:8001`
- Check browser console for specific error
- Verify CORS headers in response

---

## Deployment Verification

**All 4 Tests Passed ✅**
```
1️⃣ LOGIN endpoint ✓
2️⃣ ADD-PATIENT endpoint ✓
3️⃣ GET-PATIENTS endpoint ✓
4️⃣ HEALTH endpoints ✓
```

**Total Patients in DB:** 4
**Latest Patient:** PAT004

---

## Next Steps (Optional)

1. **Security:** Replace hardcoded admin credentials with database lookup
2. **Scalability:** Add caching and rate limiting
3. **Features:** Add appointment status updates, cancellation, rescheduling
4. **UI:** Add mobile-responsive design
5. **Monitoring:** Add logging and error tracking

---

## Support

All code is documented in:
- **Backend:** See docstrings in `main.py`
- **Frontend:** See comments in `script-jwt.js`
- **API Docs:** http://127.0.0.1:8001/docs

---

**Deployed:** 2026-06-19 ✅
