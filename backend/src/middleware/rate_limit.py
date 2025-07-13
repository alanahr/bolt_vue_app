from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
from collections import defaultdict, deque
import os

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 900):
        super().__init__(app)
        self.calls = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", calls))
        self.period = int(os.getenv("RATE_LIMIT_WINDOW_MS", period * 1000)) // 1000
        self.clients = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path.startswith("/health"):
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests
        client_requests = self.clients[client_ip]
        while client_requests and client_requests[0] <= current_time - self.period:
            client_requests.popleft()
        
        # Check rate limit
        if len(client_requests) >= self.calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )
        
        # Add current request
        client_requests.append(current_time)
        
        response = await call_next(request)
        return response