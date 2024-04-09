import time

from celery import shared_task
from celery.result import AsyncResult


# TODO
# ! This works
# ! But not async | I can obviouly do this in the same function dummy
def test_print(id, result):
    print("result: " + str(result), flush=True)


def test():
    a: AsyncResult[int] = testing.apply_async()
    # Use propagate=False to avoid raising exceptions. Check if failed by a.failed()
    a.get(propagate=False, callback=test_print)
    print("async?")


@shared_task
def testing():
    time.sleep(2)
    return 5
