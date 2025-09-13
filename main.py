import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import asyncio, webbrowser

# Initialize FastAPI app
app = FastAPI(title="Sustainable Farming AI System")

# Database setup
DATABASE_URL = "sqlite:///farming.db"
engine = create_engine(DATABASE_URL, echo=True)

# Ensure tables exist using schema file
with open("database_schema.sql", "r") as f:
    schema_sql = f.read()
with engine.connect() as conn:
    for stmt in schema_sql.split(";"):
        if stmt.strip():
            conn.execute(text(stmt))
    conn.commit()

# Load datasets
try:
    farmer_data = pd.read_csv("farmer_advisor_dataset.csv")
except FileNotFoundError:
    farmer_data = pd.DataFrame()

try:
    market_data = pd.read_csv("market_researcher_dataset.csv")
except FileNotFoundError:
    market_data = pd.DataFrame()

# Pydantic models
class FarmerInput(BaseModel):
    name: str
    location: str
    farm_size: float
    soil_type: str
    water_availability: str
    preferred_crops: Optional[List[str]] = None
    budget: float

# Serve static files (so farmer_profile.html is accessible)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def home():
    return FileResponse("farmer_profile.html")

# API: Create farmer profile
@app.post("/api/farmers/")
async def create_farmer(farmer: FarmerInput):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO farmers (name, location, farm_size, soil_type, water_availability)
                    VALUES (:name, :location, :farm_size, :soil_type, :water_availability)
                """),
                {
                    "name": farmer.name,
                    "location": farmer.location,
                    "farm_size": farmer.farm_size,
                    "soil_type": farmer.soil_type,
                    "water_availability": farmer.water_availability,
                }
            )
            farmer_id = result.lastrowid
            conn.commit()
        return {"farmer_id": farmer_id, "message": "Profile created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API: Simple recommendations endpoint
@app.get("/recommendations/{farmer_id}")
async def recommendations(farmer_id: int):
    return {
        "farmer_id": farmer_id,
        "recommended_crop": "Rice",
        "note": "Future: integrate soil + market analysis"
    }

# Auto-open browser on startup
@app.on_event("startup")
async def startup_event():
    await asyncio.sleep(1)  # give server time to start
    webbrowser.open("http://127.0.0.1:8000")

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
