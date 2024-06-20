import threading
import datetime
import time

from functools import wraps
from typing import ParamSpec, TypeVar, Callable, Generic, Self, Optional, overload

try:
    from constants.constants import ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS
except:
    ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS = datetime.time(0,0,0,0)

__all__ = [
    'periodic_function_call',
    'function_logger'
]

__F_Spec__ = ParamSpec("__F_Spec__")
__F_Return__ = TypeVar("__F_Return__")

class __PeriodicFunctionCall__(Generic[__F_Spec__, __F_Return__]):
    wrapped_call: Callable[__F_Spec__, __F_Return__]
    caller: Callable[__F_Spec__, __F_Return__]
    call_result: __F_Return__
    call_create_buf: bool
    decorators: list[object]
    interval_in_seconds: int
    target_time: Optional[datetime.time]

    def __new__(
            cls,
            call: Callable[__F_Spec__, __F_Return__],
            interval_in_seconds: int,
            call_return: bool,
            target_time: Optional[datetime.time],
            ) -> Self:
            if isinstance(call, __PeriodicFunctionCall__):
                return call
            return super().__new__(cls)

    def __init__(
            self,
            call: Callable[__F_Spec__, __F_Return__],
            interval_in_seconds: int,
            call_return: bool,
            target_time: Optional[datetime.time]
            ) -> None:
        if not isinstance(call, __PeriodicFunctionCall__):
            self.interval_in_seconds = interval_in_seconds
            self.wrapped_call = call
            self.decorators = []
            self.call_result = None
            self.call_create_buf = call_return
            if target_time:
                self.target_time = target_time
            else:
                self.target_time = ACCRUAL_START_TIME_OF_AUTOTRANSACTIONS
        else:
            if call in self.decorators:
                raise ValueError(f"The decorator \"periodic_function_call\" is already applied to {call.wrapped_call.__name__}. "
                                 "Unable to apply the decorator multiple times to the same function.")
        self.decorators.append(self)

        @wraps(self.wrapped_call)
        def caller(
            *args: __F_Spec__.args,
            **kwargs: __F_Spec__.kwargs
            ) -> __F_Return__:
            return self.wrapped_call(*args, **kwargs)

        self.caller = caller

        @wraps(self.wrapped_call)
        def wrapper(
            *args: __F_Spec__.args,
            **kwargs: __F_Spec__.kwargs
            ) -> None:
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
            ) -> Optional[__F_Return__]:
        if self.call_create_buf:
            self.call_result = self.caller(*args, **kwargs)
            self.call_create_buf = False
        return self.call_result

def periodic_function_call(
        interval_in_seconds: int,
        target_time: Optional[datetime.time] = None,
        *,
        call_return: Optional[bool] = False
        ) -> Callable[[Callable[__F_Spec__, __F_Return__]], __PeriodicFunctionCall__[__F_Spec__, __F_Return__]]:
    def decorator(func: Callable[__F_Spec__, __F_Return__]) -> __PeriodicFunctionCall__[__F_Spec__, __F_Return__]:
        return __PeriodicFunctionCall__(func, interval_in_seconds, call_return, target_time)
    return decorator

class __FunctionLogger__(Generic[__F_Spec__, __F_Return__]):
    wrapped_call: Callable[__F_Spec__, __F_Return__]
    decorators: list[object]
    name_log_file: list[str]

    def __new__(
            cls,
            call: Callable[__F_Spec__, __F_Return__],
            name_log_file: Optional[str]
            ) -> Self:
        if isinstance(call, __FunctionLogger__):
            return call
        return super().__new__(cls)

    def __init__(
            self,
            call: Callable[__F_Spec__, __F_Return__],
            name_log_file: str
            ) -> None:
        if isinstance(call, __FunctionLogger__):
            if call in self.decorators:
                if name_log_file in call.name_log_file:
                    raise ValueError(f"Logs about the function \"{call.wrapped_call.__name__}\" "
                                     f"in file \"{name_log_file}\" are already being maintained!")
            self.name_log_file.append(name_log_file)
        else:
            self.wrapped_call = call
            self.decorators = []
            self.name_log_file = [name_log_file]
        self.decorators.append(self)

    def __call__(
            self,
            *args: __F_Spec__.args,
            **kwargs: __F_Spec__.kwargs
            ) -> __F_Return__:
        result = self.wrapped_call(*args, **kwargs)
        log_label = f"{datetime.datetime.today()} - function \"{self.wrapped_call.__name__}\" returned {result};\n"
        for ways in self.name_log_file:
            with open(ways, "a") as f:
                f.write(log_label)
        return result

def __function_logger_wrapper__(
        name_log_file: str|None
        ) -> Callable[[Callable[__F_Spec__, __F_Return__]], __FunctionLogger__[__F_Spec__, __F_Return__]]:
    def decorator(func: Callable[__F_Spec__, __F_Return__]) -> __FunctionLogger__[__F_Spec__, __F_Return__]:
        if name_log_file:
            return __FunctionLogger__(func, name_log_file)
        return __FunctionLogger__(func, "log.log")
    return decorator

@overload
def function_logger(
    call: Callable[__F_Spec__, __F_Return__],
    *,
    name_log_file: Optional[str] = None
) -> Callable[__F_Spec__, __F_Return__]:
    ...

@overload
def function_logger(
    call: None = None,
    *,
    name_log_file: Optional[str] = None
) -> Callable[
    [Callable[__F_Spec__, __F_Return__]],
    Callable[__F_Spec__, __F_Return__]
]: ... 

def function_logger(
        func: Optional[Callable[__F_Spec__, __F_Return__]] = None,
        *,
        name_log_file: Optional[str] = None
    ) -> Callable[
        [Callable[__F_Spec__, __F_Return__]],
        Callable[__F_Spec__, __F_Return__]
    ] | Callable[
        __F_Spec__,
        __F_Return__
    ]:
    wrap_decorator = __function_logger_wrapper__(name_log_file)
    if func is None:
        return wrap_decorator
    return wrap_decorator(func)
x = datetime.time(1)
"""
@periodic_function_call(30, datetime.time(20, 8, 0, 0))
def test() -> None:
    print("ok")

@function_logger(name_log_file="log2.log")
@function_logger
def test2(s: int = 0) -> bool:
    if s > 0: return True
    return False

import random
while(True):
    test()
    test2(random.randint(-1000, 1000))
    time.sleep(10)
"""