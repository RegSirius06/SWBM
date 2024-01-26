import threading
import datetime
import time

from functools import wraps
from typing import ParamSpec, TypeVar, Callable, Generic, Self, Optional

try:
    from constants.constants import ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS
except:
    ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS = datetime.time(0,0,0,0)

__F_Spec__ = ParamSpec("__F_Spec__")
__F_Return__ = TypeVar("__F_Return__")

class __PeriodicFunctionCall__(Generic[__F_Spec__, __F_Return__]):
    wrapped_call: Callable[__F_Spec__, __F_Return__]
    decorators: list[object]
    interval_in_seconds: int
    target_time: Optional[datetime.time]

    def __new__(
            cls,
            call: Callable[__F_Spec__, __F_Return__],
            interval_in_seconds: int,
            target_time: Optional[datetime.time]
            ) -> Self:
            if isinstance(call, __PeriodicFunctionCall__):
                return call
            return super().__new__(cls)

    def __init__(
            self,
            call: Callable[__F_Spec__, __F_Return__],
            interval_in_seconds: int,
            target_time: Optional[datetime.time]
            ) -> None:
        if not isinstance(call, __PeriodicFunctionCall__):
            self.interval_in_seconds = interval_in_seconds
            self.wrapped_call = call
            self.decorators = []
            if target_time:
                self.target_time = target_time
            else:
                self.target_time = ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS
        else:
            if call in self.decorators:
                raise ValueError(f"The decorator is already applied to {call.wrapped_call.__name__}. "
                                 "Unable to apply the decorator multiple times to the same function.")
        self.decorators.append(self)

        @wraps(self.wrapped_call)
        def wrapper(
            *args: __F_Spec__.args,
            **kwargs: __F_Spec__.kwargs
            ) -> __F_Return__:
            flag = True
            while True:
                if flag:
                    current_time = datetime.datetime.now().time()
                    now = datetime.datetime.combine(datetime.date.today(), current_time)
                    target = datetime.datetime.combine(datetime.date.today(), target_time)
                    if now > target:
                        target += datetime.timedelta(days=1)
                    time_to_sleep = (target - now).total_seconds()
                    time.sleep(time_to_sleep)
                    flag = False
                self.wrapped_call(*args, **kwargs)
                time.sleep(self.interval_in_seconds)
        t = threading.Thread(target=wrapper, args=())
        t.daemon = True
        t.start()

    def __call__(
            self,
            *args: __F_Spec__.args,
            **kwargs: __F_Spec__.kwargs
            ) -> __F_Return__:
        return self.wrapped_call(*args, **kwargs)

def periodic_function_call(
        interval_in_seconds: int,
        target_time: Optional[datetime.time] = None
        ) -> Callable[[Callable[__F_Spec__, __F_Return__]], __PeriodicFunctionCall__[__F_Spec__, __F_Return__]]:
    def decorator(func: Callable[__F_Spec__, __F_Return__]) -> __PeriodicFunctionCall__[__F_Spec__, __F_Return__]:
        return __PeriodicFunctionCall__(func, interval_in_seconds, target_time)
    return decorator
