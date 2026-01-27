import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        
        # Attach to request state
        request.state.request_id = request_id

        response = await call_next(request)

        # Return it in response headers
        response.headers["X-Request-ID"] = request_id

        return response