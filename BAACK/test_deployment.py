import urllib.request, json

print("=" * 60)
print("TESTING CARELINECLINIC APP FULL FLOW")
print("=" * 60)

# Step 1: Login
print("\n1️⃣ Testing LOGIN endpoint...")
try:
    login_data = json.dumps({"username": "admin", "password": "password"}).encode()
    login_req = urllib.request.Request("http://127.0.0.1:8001/login", data=login_data, headers={"Content-Type": "application/json"})
    login_resp = urllib.request.urlopen(login_req)
    login_result = json.loads(login_resp.read())
    token = login_result["access_token"]
    print("✓ LOGIN SUCCESSFUL")
    print(f"  Token: {token[:40]}...")
except Exception as e:
    print(f"✗ LOGIN FAILED: {e}")
    exit(1)

# Step 2: Add Patient
print("\n2️⃣ Testing ADD-PATIENT endpoint...")
try:
    patient_data = json.dumps({
        "patient_name": "Test Deploy",
        "mobile_number": "9876543210",
        "appointment_date": "2026-06-20",
        "appointment_time": "14:00"
    }).encode()
    
    patient_req = urllib.request.Request(
        "http://127.0.0.1:8001/add-patient",
        data=patient_data,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    )
    patient_resp = urllib.request.urlopen(patient_req)
    patient_result = json.loads(patient_resp.read())
    print("✓ PATIENT CREATED SUCCESSFULLY")
    print(f"  Patient ID: {patient_result['patient_id']}")
    print(f"  Name: {patient_result['patient_name']}")
    print(f"  Unique ID: {patient_result['unique_id']}")
    print(f"  Status: {patient_result['status']}")
except Exception as e:
    print(f"✗ ADD-PATIENT FAILED: {e}")
    exit(1)

# Step 3: Get Patients
print("\n3️⃣ Testing GET-PATIENTS endpoint...")
try:
    patients_req = urllib.request.Request(
        "http://127.0.0.1:8001/patients",
        headers={"Authorization": f"Bearer {token}"}
    )
    patients_resp = urllib.request.urlopen(patients_req)
    patients_list = json.loads(patients_resp.read())
    print("✓ PATIENTS RETRIEVED SUCCESSFULLY")
    print(f"  Total patients in database: {len(patients_list)}")
    print(f"  Latest patient: {patients_list[-1]['patient_id']} - {patients_list[-1]['patient_name']}")
except Exception as e:
    print(f"✗ GET-PATIENTS FAILED: {e}")
    exit(1)

# Step 4: Test health check
print("\n4️⃣ Testing HEALTH endpoints...")
try:
    health_req = urllib.request.Request("http://127.0.0.1:8001/ping")
    health_resp = urllib.request.urlopen(health_req)
    health_result = json.loads(health_resp.read())
    print("✓ PING ENDPOINT WORKING")
    print(f"  Status: {health_result}")
except Exception as e:
    print(f"✗ HEALTH CHECK FAILED: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - APP IS READY FOR DEPLOYMENT")
print("=" * 60)
