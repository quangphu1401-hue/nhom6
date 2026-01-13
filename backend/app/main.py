from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import crops, weather, care_logs, pests, analytics, ai_assistant
from app.database.database import engine, Base
from app.models import crop_model, weather_model, care_log_model, pest_model, season_history_model
import os
from dotenv import load_dotenv

load_dotenv()

# Tạo database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroBI API",
    description="Hệ thống Kinh Doanh Thông Minh Nông Nghiệp - API Backend",
    version="1.0.0"
)

# CORS Configuration
from app.config import settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crops.router, prefix="/api/crops", tags=["Crops"])
app.include_router(weather.router, prefix="/api/weather", tags=["Weather"])
app.include_router(care_logs.router, prefix="/api/care-logs", tags=["Care Logs"])
app.include_router(pests.router, prefix="/api/pests", tags=["Pests"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(ai_assistant.router, prefix="/api/ai", tags=["AI Assistant"])

@app.get("/")
async def root():
    return {
        "message": "AgroBI API - Hệ thống Kinh Doanh Thông Minh Nông Nghiệp",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

