from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response: Response = await call_next(request)
            return response
        except HTTPException as http_err:
            return Response(
                content=f"HTTP error occurred: {str(http_err)}",
                status_code=http_err.status_code,
            )
        except Exception as err:
            return Response(
                content=f"An unexpected error occurred: {str(err)}", status_code=500
            )
