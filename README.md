# CareLine Clinic - Quick Setup

## 🚀 Deploy in 2 Minutes

### Step 1: Install Dependencies
```bash
cd BAACK
pip install -r requirements.txt
```

### Step 2: Run Everything
**Windows:** Double-click `START_APP.bat`

**Or manually:**
```bash
# Terminal 1: Start Backend
cd BAACK
python -m uvicorn main:app --reload --port 8001

# Terminal 2: Start Frontend
cd FRONT
python -m http.server 5500
```

### Step 3: Access the App
- **Frontend:** http://127.0.0.1:5500
- **Backend Docs:** http://127.0.0.1:8001/docs
- **Login:** admin / password

---

## 📋 What's Working

✅ User Login (JWT)
✅ Book Appointments
✅ View All Appointments
✅ Auto-generate Patient IDs
✅ Swagger API Docs
✅ Supabase Database Integration

---

## 🧪 Verify Installation

```bash
cd BAACK
python test_deployment.py
```

Should show: `✅ ALL TESTS PASSED`

---

## 📚 Documentation

- **Full Guide:** See `DEPLOYMENT_GUIDE.md`
- **API Docs:** http://127.0.0.1:8001/docs
- **Code:** Check docstrings in `main.py` and `script-jwt.js`

---

## 🎯 Demo Flow

1. Go to http://127.0.0.1:5500
2. Login: `admin` / `password`
3. Fill appointment form
4. Click "Save & Generate ID"
5. See confirmation ticket
6. View in appointments table below

---

**Status:** ✅ Production Ready
