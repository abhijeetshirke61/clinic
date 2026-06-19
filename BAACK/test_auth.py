import urllib.request, json

# Step 1: Login to get token
login_data = json.dumps({"username": "admin", "password": "password"}).encode()
login_req = urllib.request.Request("http://127.0.0.1:8001/login", data=login_data, headers={"Content-Type": "application/json"})
login_resp = urllib.request.urlopen(login_req)
login_result = json.loads(login_resp.read())
token = login_result["access_token"]
print("✓ Token obtained:", token[:50] + "...")

# Step 2: Create patient with token
patient_data = json.dumps({
    "patient_name": "Test Patient",
    "mobile_number": "9876543210",
    "appointment_date": "2026-06-20",
    "appointment_time": "10:00"
}).encode()

patient_req = urllib.request.Request(
    "http://127.0.0.1:8001/add-patient",
    data=patient_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
)
patient_resp = urllib.request.urlopen(patient_req)
patient_result = json.loads(patient_resp.read())
print("\n✓ Patient created successfully!")
print(f"  Patient ID: {patient_result['patient_id']}")
print(f"  Name: {patient_result['patient_name']}")
print(f"  Status: {patient_result['status']}")
