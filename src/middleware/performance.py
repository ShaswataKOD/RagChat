from fastapi import Request
import time



async def measure_response_time(request: Request, call_next):

    start_time = time.perf_counter()

    response = await call_next(request)

    time_taken = time.perf_counter() - start_time

    response.headers["Process-Time"] = f"{time_taken * 1000:.2f} ms"

    return response
