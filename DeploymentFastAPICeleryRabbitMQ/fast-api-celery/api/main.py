from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
import redis

from worker.tasks import get_sunrise_sunset, is_Image_WellExposedByHisto, get_apple_automatic_rois, \
    get_apple_automatic_rois_with_indicators
from .models import SunriseSunsetInput, TaskTicket, SunriseSunsetOutput, TaskRedisRemoved
from .models import ImageWellExposedInput, ImageWellExposedOutput
from .models import AutomaticAppleSegmentationInput, AutomaticAppleSegmentationOutput, \
    AutomaticAppleSegmentationWithIndicatorsOutput

app = FastAPI()


def delete_task_from_redis(task_id):
    r = redis.Redis(host='10.0.20.50', port=6379)

    key = "celery-task-meta-" + task_id

    # Usuń klucz i sprawdź, czy udało się go usunąć
    result = r.delete(key)

    if result == 1:
        return True  # klucz został usunięty
    else:
        return False  # klucz nie istniał lub wystąpił błąd


@app.get('/Redis/delete_task_from_redis/{task_id}', response_model=TaskRedisRemoved, status_code=200)
def Redis_delete_task_from_redis(task_id):
    statusFlag1 = delete_task_from_redis(task_id)

    return TaskRedisRemoved(statusFlag=statusFlag1)


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


@app.post('/AutomaticAppleSegmentationModel/get_apple_automatic_rois', response_model=TaskTicket, status_code=202)
async def schedule_AutomaticAppleSegmentationModel_get_apple_automatic_rois(
        model_input: AutomaticAppleSegmentationInput):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    task_id = get_apple_automatic_rois.delay(model_input.imageBase64, model_input.filename,
                                             model_input.jsonBase64ImageROIs)
    # return {'task_id': str(task_id), 'status': 'Processing'}
    return TaskTicket(task_id=str(task_id), status='Processing')


@app.get('/AutomaticAppleSegmentationModel/get_apple_automatic_rois_result/{task_id}',
         response_model=AutomaticAppleSegmentationOutput,
         status_code=200,
         responses={202: {'model': TaskTicket, 'description': 'Accepted: Not Ready'}})
async def get_AutomaticAppleSegmentationModel_get_apple_automatic_rois_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        # print(app.url_path_for('schedule_prediction'))
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    filename, jsonBase64AppleROIs = result
    return AutomaticAppleSegmentationOutput(task_id=task_id, status='Success', filename=filename,
                                            jsonBase64AppleROIs=jsonBase64AppleROIs)


@app.post('/AutomaticAppleSegmentationModel/get_apple_automatic_rois_with_indicators', response_model=TaskTicket,
          status_code=202)
async def schedule_AutomaticAppleSegmentationModel_get_apple_automatic_rois_with_indicators(
        model_input: AutomaticAppleSegmentationInput):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    task_id = get_apple_automatic_rois_with_indicators.delay(model_input.imageBase64, model_input.filename,
                                                             model_input.jsonBase64ImageROIs)
    # return {'task_id': str(task_id), 'status': 'Processing'}
    return TaskTicket(task_id=str(task_id), status='Processing')


@app.get('/AutomaticAppleSegmentationModel/get_apple_automatic_rois_with_indicators_result/{task_id}',
         response_model=AutomaticAppleSegmentationWithIndicatorsOutput,
         status_code=200,
         responses={202: {'model': TaskTicket, 'description': 'Accepted: Not Ready'}})
async def get_AutomaticAppleSegmentationModel_get_apple_automatic_rois_with_indicators_result(task_id):
    """Fetch result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})

    result = task.get()
    filename, jsonBase64AppleROIs, df_local = result

    # Sprawdź, czy df_local jest pusty
    if df_local.empty:
        r_av = g_av = b_av = r_sd = g_sd = b_sd = bri_av = bri_sd = gi_av = gei_av = gei_sd = ri_av = ri_sd = bi_av = bi_sd = avg_width = avg_height = avg_area = number_of_apples = -1
    else:
        r_av = float(df_local["r.av"].iloc[0])
        g_av = float(df_local["g.av"].iloc[0])
        b_av = float(df_local["b.av"].iloc[0])
        r_sd = float(df_local["r.sd"].iloc[0])
        g_sd = float(df_local["g.sd"].iloc[0])
        b_sd = float(df_local["b.sd"].iloc[0])
        bri_av = float(df_local["bri.av"].iloc[0])
        bri_sd = float(df_local["bri.sd"].iloc[0])
        gi_av = float(df_local["gi.av"].iloc[0])
        gei_av = float(df_local["gei.av"].iloc[0])
        gei_sd = float(df_local["gei.sd"].iloc[0])
        ri_av = float(df_local["ri.av"].iloc[0])
        ri_sd = float(df_local["ri.sd"].iloc[0])
        bi_av = float(df_local["bi.av"].iloc[0])
        bi_sd = float(df_local["bi.sd"].iloc[0])
        avg_width = float(df_local["avg_width"].iloc[0])
        avg_height = float(df_local["avg_height"].iloc[0])
        avg_area = float(df_local["avg_area"].iloc[0])
        number_of_apples = int(df_local["number_of_apples"].iloc[0])

    output = AutomaticAppleSegmentationWithIndicatorsOutput(
        task_id=task_id,
        status='Success',  # zamień na prawdziwy status
        filename=filename,  # zamień na prawdziwą nazwę pliku
        jsonBase64AppleROIs=jsonBase64AppleROIs,  # zamień na prawdziwy JSON
        r_av=r_av,
        g_av=g_av,
        b_av=b_av,
        r_sd=r_sd,
        g_sd=g_sd,
        b_sd=b_sd,
        bri_av=bri_av,
        bri_sd=bri_sd,
        gi_av=gi_av,
        gei_av=gei_av,
        gei_sd=gei_sd,
        ri_av=ri_av,
        ri_sd=ri_sd,
        bi_av=bi_av,
        bi_sd=bi_sd,
        avg_width=avg_width,
        avg_height=avg_height,
        avg_area=avg_area,
        number_of_apples=number_of_apples
    )

    return output
