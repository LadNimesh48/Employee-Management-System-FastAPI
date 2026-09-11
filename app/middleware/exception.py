from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse


async def exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response

    except HTTPException as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content={"status": False, "message": exc.detail, "data": None},
        )

    except Exception as exc:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": False, "message": str(exc), "data": None},
        )
