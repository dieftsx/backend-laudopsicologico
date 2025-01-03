from fastapi import Request, HTTPException
import time
from collections import defaultdict
from ..config.settings import settings


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.window = settings.RATE_LIMIT_WINDOW
        self.max_requests = settings.RATE_LIMIT_MAX_REQUESTS

    async def __call__(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Limpar requisições antigas
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < self.window
        ]

        # Verificar limite
        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )

        # Adicionar nova requisição
        self.requests[client_ip].append(current_time)

        return await call_next(request)