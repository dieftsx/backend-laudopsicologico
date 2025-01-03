from fastapi import Request
import time
import logging
from ..config.settings import settings
import json

logging.basicConfig(
    filename=settings.LOG_FILE,
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


async def logging_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    log_dict = {
        "path": request.url.path,
        "method": request.method,
        "process_time": process_time,
        "status_code": response.status_code,
        "client_host": request.client.host if request.client else None,
    }

    logging.info(json.dumps(log_dict))

    return response