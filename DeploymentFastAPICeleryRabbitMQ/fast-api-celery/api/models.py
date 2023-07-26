from pydantic import BaseModel
from datetime import datetime
import numpy as np
from typing import Optional

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
    UTCsunrise: datetime
    UTCsunset: datetime


class ImageWellExposedInput(BaseModel):
    """Model features as input for prediction"""
    imageBase64: str  # base64 encoded image
    filename: str
    lat: float
    lon: float
    UTCdate: datetime


class ImageWellExposedOutput(BaseModel):
    """Final result"""
    task_id: str
    status: str
    WellExposedStatusFlag: bool
    WellExposedStatusDesc: str
    filename: str


class AutomaticAppleSegmentationInput(BaseModel):
    """Model features as input for prediction"""
    imageBase64: str  # base64 encoded image
    filename: str
    jsonBase64ImageROIs: Optional[str] = None   # optional parameter

class AutomaticAppleSegmentationOutput(BaseModel):
    """Model features as input for prediction"""
    task_id: str
    status: str
    filename: str
    jsonBase64AppleROIs: str
