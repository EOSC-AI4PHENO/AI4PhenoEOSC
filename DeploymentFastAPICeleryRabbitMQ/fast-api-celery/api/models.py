from pydantic import BaseModel
from datetime import datetime

class TaskTicket(BaseModel):
    """ID and status for the async tasks"""
    task_id: str
    status: str

class SunriseSunsetInput(BaseModel):
    """Model features as input for prediction"""
    # x: float
    lat: float
    lon: float
    UTCdate: datetime

class SunriseSunsetOutput(BaseModel):
    """Final result"""
    task_id: str
    status: str
    result: tuple[datetime, datetime]
