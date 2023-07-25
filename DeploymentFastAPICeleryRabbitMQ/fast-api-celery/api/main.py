from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from celery.result import AsyncResult

from worker.tasks import get_sunrise_sunset, is_Image_WellExposedByHisto
from .models import SunriseSunsetInput, TaskTicket, SunriseSunsetOutput
from .models import ImageWellExposedInput, ImageWellExposedOutput

app = FastAPI()


@app.post('/ImageWellExposedModel/is_Image_WellExposedByHisto', response_model=TaskTicket, status_code=202)
async def schedule_ImageWellExposedModel_is_Image_WellExposedByHisto(model_input: ImageWellExposedInput):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    task_id = is_Image_WellExposedByHisto.delay(model_input.imageBase64, model_input.filename, model_input.lat,
                                                model_input.lon, model_input.UTCdate)
    # return {'task_id': str(task_id), 'status': 'Processing'}
    return TaskTicket(task_id=str(task_id), status='Processing')


@app.get('/ImageWellExposedModel/is_Image_WellExposedByHisto_result/{task_id}', response_model=ImageWellExposedOutput,
         status_code=200,
         responses={202: {'model': TaskTicket, 'description': 'Accepted: Not Ready'}})
async def get_ImageWellExposedModel_is_Image_WellExposedByHisto_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        # print(app.url_path_for('schedule_prediction'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    WellExposedStatusFlag, WellExposedStatusDesc, filename = result
    # return {'task_id': task_id, 'status': 'Success', 'WellExposedStatusFlag': WellExposedStatusFlag,'WellExposedStatusDesc': WellExposedStatusDesc,}
    return ImageWellExposedOutput(task_id=task_id, status='Success', WellExposedStatusFlag=WellExposedStatusFlag,
                                  WellExposedStatusDesc=WellExposedStatusDesc, filename=filename)


@app.post('/ImageWellExposedModel/get_sunrise_sunset', response_model=TaskTicket, status_code=202)
async def schedule_ImageWellExposedModel_get_sunrise_sunset(model_input: SunriseSunsetInput):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    task_id = get_sunrise_sunset.delay(model_input.lat, model_input.lon, model_input.UTCdate)
    # return {'task_id': str(task_id), 'status': 'Processing'}
    return TaskTicket(task_id=str(task_id), status='Processing')


@app.get('/ImageWellExposedModel/get_sunrise_sunset_result/{task_id}', response_model=SunriseSunsetOutput,
         status_code=200,
         responses={202: {'model': TaskTicket, 'description': 'Accepted: Not Ready'}})
async def get_ImageWellExposedModel_get_sunrise_sunset_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        # print(app.url_path_for('schedule_prediction'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    UTCsunrise, UTCsunset = result
    # return {'task_id': task_id, 'status': 'Success', 'UTCsunrise': UTCsunrise, 'UTCsunset': UTCsunset}
    return SunriseSunsetOutput(task_id=task_id, status='Success', UTCsunrise=UTCsunrise, UTCsunset=UTCsunset)
