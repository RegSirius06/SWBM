import threading
import datetime
import time

from functools import wraps
from typing import ParamSpec, TypeVar, Callable

from constants.constants import ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS

F_Spec = ParamSpec("F_Spec")
F_Return = TypeVar("F_Return")

def periodic_function_call(interval_in_seconds: int) -> Callable[[Callable[F_Spec, F_Return]], None]:
    def decorator(func: Callable[F_Spec, F_Return]) -> None:
        @wraps(func)
        def wrapper(*args: F_Spec.args, **kwargs: F_Spec.kwargs) -> F_Return:
            flag = True
            while True:
                if flag:
                    current_time = datetime.datetime.now().time()
                    target_time = ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS
                    if current_time < target_time:
                        delta = datetime.datetime.combine(datetime.date.today(), target_time) - datetime.datetime.combine(datetime.date.today(), current_time)
                    else:
                        next_day = datetime.date.today() + datetime.timedelta(days=1)
                        delta = datetime.datetime.combine(next_day, target_time) - datetime.datetime.combine(datetime.date.today(), current_time)
                    time_to_sleep = delta.total_seconds()
                    time.sleep(time_to_sleep)
                    flag = False
                func(*args, **kwargs)
                time.sleep(interval_in_seconds)
        t = threading.Thread(target=wrapper, args=())
        t.daemon = True
        t.start()
        return wrapper
    return decorator
"""
@periodic_function_call(30)
def function() -> None:
    print("CCC")

while True:
    time.sleep(1) # имитация основного потока
"""