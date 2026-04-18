from fastapi import FastAPI
from fastapi import  HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime, timezone

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/message/")
async def root():
    return {"message": "Hello World"}


@app.get("/")
def index():
    return {"message": "I'm new to this so HELLO World!"}


@app.get("/api/classify")

def classify(name: str):
    if not isinstance(name, str):
        raise HTTPException(
            status_code=422,
            detail={"status": "error", "message": "Name must be a string"}
        )
    
    if name.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "Name is required"}
        )

    try:
        response = requests.get(f"https://api.genderize.io/?name={name}", timeout=5)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail={"status": "error", "message": "Failed to fetch data from Genderize API"}
            )
        
        data = response.json()

    except requests.exceptions.RequestException:
        raise HTTPException(
            status_code=502,
            detail={"status": "error", "message": "External API request failed"}
        )

    gender = data.get("gender")
    probability = data.get("probability")
    count = data.get("count")

    if gender is None or count == 0:
        return {
            "status": "error",
            "message": "No prediction available for the provided name"
        }

    sample_size = count
    is_confident = probability >= 0.7 and sample_size >= 100

    processed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return {
        "status": "success",
        "data": {
            "name": name,
            "gender": gender,
            "probability": probability,
            "sample_size": sample_size,
            "is_confident": is_confident,
            "processed_at": processed_at
        }
    }

handler = app