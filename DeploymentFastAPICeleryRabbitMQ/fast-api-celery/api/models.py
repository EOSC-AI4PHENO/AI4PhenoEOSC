from pydantic import BaseModel
from datetime import datetime
import numpy as np

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

class ImageWellExposedInput(BaseModel):
    """Model features as input for prediction"""
    imageBase64: str  # base64 encoded image
    lat: float
    lon: float
    UTCdate: datetime

class ImageWellExposedOutput(BaseModel):
    """Final result"""
    task_id: str
    status: str
    result: tuple[bool, str]
