from pydantic import BaseModel
from datetime import datetime
import numpy as np
from typing import Optional
from typing import List

class TaskRedisRemoved(BaseModel):
    """ID and status for the async tasks"""
    statusFlag: bool


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
    jsonBase64ImageROIs: Optional[str] = None  # optional parameter


class AutomaticAppleSegmentationOutput(BaseModel):
    """Model features as input for prediction"""
    task_id: str
    status: str
    filename: str
    jsonBase64AppleROIs: str


class AutomaticAppleSegmentationWithIndicatorsOutput(BaseModel):
    """Model features as input for prediction"""
    task_id: str
    status: str
    filename: str
    jsonBase64AppleROIs: str
    r_av: float
    g_av: float
    b_av: float
    r_sd: float
    g_sd: float
    b_sd: float
    bri_av: float
    bri_sd: float
    gi_av: float
    gei_av: float
    gei_sd: float
    ri_av: float
    ri_sd: float
    bi_av: float
    bi_sd: float
    avg_width: float
    avg_height: float
    avg_area: float
    number_of_apples: int

class LindenClassificationInput(BaseModel):
    """Model features as input for prediction"""
    imageBase64: str  # base64 encoded image
    filename: str
    jsonBase64ImageROIs: str

class LindenClassificationOutput(BaseModel):
    """Model features as input for prediction"""
    task_id: str
    status: str
    filename: str
    isfloweringList:  List[bool]
