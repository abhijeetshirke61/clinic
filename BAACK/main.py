from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from database import supabase
import jwt
from datetime import datetime, timedelta
from typing import Optional, List

app = FastAPI(
    title="CareLine Clinic API",
    description="Patient appointment booking and management system with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ⭐ MUST BE HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5501", "http://localhost:5501", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = "HlFQwCw7drCfhk6DQsM1DMX5gY9Hx379Ah5y3tEaNwPlrXg/sCLeyGg0kUwYZnBTM89qgoS7LVlWCfEv3dRSgA=="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Data Models with Swagger Documentation
class Patient(BaseModel):
    """Patient appointment booking model"""
    patient_name: str = Field(..., description="Full name of the patient", example="Abhijeet Shirke")
    mobile_number: str = Field(..., description="Patient mobile phone number", example="9999999999")
    appointment_date: str = Field(..., description="Appointment date in YYYY-MM-DD format", example="2026-06-19")
    appointment_time: str = Field(..., description="Appointment time in HH:MM format", example="14:30")
    
    class Config:
        json_schema_extra = {
            "example": {
                "patient_name": "Abhijeet Shirke",
                "mobile_number": "8010161918",
                "appointment_date": "2026-06-19",
                "appointment_time": "15:40"
            }
        }

class Login(BaseModel):
    """User login credentials"""
    username: str = Field(..., description="Username for authentication", example="admin")
    password: str = Field(..., description="Password for authentication", example="password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "password"
            }
        }

class Token(BaseModel):
    """JWT token response"""
    access_token: str = Field(..., description="JWT access token for authenticated requests")
    token_type: str = Field(..., description="Token type (always 'bearer')", example="bearer")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class PatientResponse(BaseModel):
    """Patient record as returned from database"""
    id: int = Field(..., description="Internal database ID")
    patient_id: str = Field(..., description="Generated patient ID (PAT001, PAT002, etc.)")
    patient_name: str = Field(..., description="Patient full name")
    mobile_number: str = Field(..., description="Patient phone number")
    appointment_date: str = Field(..., description="Appointment date")
    appointment_time: str = Field(..., description="Appointment time")
    status: str = Field(..., description="Appointment status", example="scheduled")
    unique_id: str = Field(..., description="Unique UUID for this appointment")
    notes: Optional[str] = Field(None, description="Additional notes about the appointment")
    created_at: str = Field(..., description="Timestamp when record was created")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_id": "PAT001",
                "patient_name": "Abhijeet Shirke",
                "mobile_number": "8010161918",
                "appointment_date": "2026-06-19",
                "appointment_time": "15:40:00",
                "status": "scheduled",
                "unique_id": "3a172d2c-b3d8-4936-8d2c-0d19dff79b27",
                "notes": None,
                "created_at": "2026-06-19T09:18:40.447763"
            }
        }

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error description")

class HealthResponse(BaseModel):
    """Health check response"""
    ok: bool = Field(..., description="Health status", example=True)

class StatusResponse(BaseModel):
    """Status message response"""
    message: str = Field(..., description="Status message")


# JWT Helper Functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    return verify_token(token)


@app.post("/login", response_model=Token, 
          summary="User Login",
          tags=["Authentication"],
          responses={
              200: {"description": "Login successful, returns JWT token"},
              401: {"model": ErrorResponse, "description": "Invalid credentials"}
          })
def login(credentials: Login):
    """
    **Authenticate user and return JWT token**
    
    Takes username and password, validates them, and returns a JWT token that must be used in the Authorization header for subsequent API calls.
    
    **Demo Credentials:**
    - Username: `admin`
    - Password: `password`
    
    **Token Usage:**
    Include the token in the Authorization header of subsequent requests:
    ```
    Authorization: Bearer <your_jwt_token>
    ```
    
    **Token Expiry:** 60 minutes
    """
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "password"
    
    if credentials.username != ADMIN_USERNAME or credentials.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": credentials.username})
    return {"access_token": access_token, "token_type": "bearer"}



@app.get("/", response_model=StatusResponse,
         summary="Health Check",
         tags=["System"],
         responses={
             200: {"description": "Server is running"}
         })
def home():
    """
    **Check if the API is running**
    
    Simple endpoint to verify the backend service is operational.
    """
    return {"message": "running"}


@app.get("/ping", response_model=HealthResponse,
         summary="Ping Service",
         tags=["System"],
         responses={
             200: {"description": "Ping successful"}
         })
def ping():
    """
    **Ping the API for connectivity check**
    
    Returns `{"ok": true}` if the server is reachable. Useful for CORS testing and client-side connectivity validation.
    """
    return {"ok": True}


@app.post("/add-patient", response_model=PatientResponse,
          summary="Add New Patient Appointment",
          tags=["Appointments"],
          responses={
              200: {"description": "Patient record created successfully"},
              400: {"model": ErrorResponse, "description": "Invalid JSON in request body"},
              401: {"model": ErrorResponse, "description": "Unauthorized - missing or invalid JWT token"},
              422: {"model": ErrorResponse, "description": "Validation error in patient data"},
              500: {"model": ErrorResponse, "description": "Database error"}
          })
async def add_patient(patient: Patient, current_user: str = Depends(get_current_user)):
    """
    **Create a new patient appointment**
    
    **Required Fields:**
    - `patient_name` (string): Full name of the patient
    - `mobile_number` (string): 10-digit phone number
    - `appointment_date` (string): Date in YYYY-MM-DD format
    - `appointment_time` (string): Time in HH:MM format
    
    **Automatic Generation:**
    - `patient_id`: Automatically generated as PAT001, PAT002, etc.
    - `unique_id`: UUID generated for appointment tracking
    - `status`: Set to "scheduled" by default
    - `created_at`: Current timestamp
    
    **Authentication:**
    Requires valid JWT token in Authorization header. Obtain token from `/login` endpoint.
    
    **Response:**
    Returns the complete patient record including generated IDs and timestamps.
    """
    try:
        # Generate patient_id by counting existing rows
        existing = supabase.table("patients").select("id", count="exact").execute()
        next_id = len(existing.data) + 1
        patient_id = f"PAT{next_id:03d}"
        
        response = supabase.table("patients").insert({
            "patient_id": patient_id,
            "patient_name": patient.patient_name,
            "mobile_number": patient.mobile_number,
            "appointment_date": patient.appointment_date,
            "appointment_time": patient.appointment_time
        }).execute()
    except Exception as e:
        print("[add-patient] Database error:", e)
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return response.data[0]


@app.get("/patients", response_model=List[PatientResponse],
         summary="Get All Patients",
         tags=["Appointments"],
         responses={
             200: {"description": "List of all patient appointments"},
             401: {"model": ErrorResponse, "description": "Unauthorized - missing or invalid JWT token"}
         })
def get_patients(current_user: str = Depends(get_current_user)):
    """
    **Retrieve all patient appointments**
    
    **Parameters:**
    - `Authorization` (header): Bearer JWT token (required)
    
    **Returns:**
    Array of all patient appointment records from the database. Each record includes:
    - Patient identification (id, patient_id)
    - Contact information (patient_name, mobile_number)
    - Appointment details (date, time)
    - Status and tracking (status, unique_id)
    - Metadata (created_at, notes)
    
    **Authentication:**
    Requires valid JWT token in Authorization header.
    """
    return supabase.table("patients").select("*").execute().data