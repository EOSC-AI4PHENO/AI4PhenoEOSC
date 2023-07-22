import importlib
import sys
import logging
from celery import Task
from .celery import worker
from datetime import datetime


class PredictTask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logging.info('Loading Model...')
            sys.path.append("..")
            module_import = importlib.import_module(self.path[0])
            model_obj = getattr(module_import, self.path[1])
            self.model = model_obj()
            logging.info('Model loaded')
        return self.run(*args, **kwargs)


@worker.task(ignore_result=False,
             bind=True,
             base=PredictTask,
             path=('logic.model', 'ImageWellExposedModel'),
             name='{}.{}'.format(__name__, 'ImageWellExposed'))

def convert_to_datetime(date_str):
    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %H:%M:%S.%f%z"]

    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass

    raise ValueError("Nieznany format daty: {}".format(date_str))


def get_sunrise_sunset(self, lat: float, lon: float, UTCdate: datetime):
    UTCdate = convert_to_datetime(UTCdate)
    a2 = UTCdate.strftime('%Y/%m/%d')
    return self.model.get_sunrise_sunset(lat, lon, UTCdate)
