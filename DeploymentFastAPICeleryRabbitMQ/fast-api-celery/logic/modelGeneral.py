import redis

class GeneralModel:
    def __init__(self):
        self.m = 7.0  # not used only example
        self.q = 0.5  # not used only example

    def delete_task_from_redis(self, task_id) -> bool:
        r = redis.Redis(host='10.0.20.50', port=6379)

        key = "celery-task-meta-" + task_id

        # Usuń klucz i sprawdź, czy udało się go usunąć
        result = r.delete(key)

        if result == 1:
            return True  # klucz został usunięty
        else:
            return False  # klucz nie istniał lub wystąpił błąd


# # Tworzę instancję klasy GeneralModel
# model = GeneralModel()
#
# # Przykład użycia:
# task_id = "8edc295a-ae52-4529-9698-95d0cf376510"
# result = model.delete_task_from_redis(task_id)
# print(result)
