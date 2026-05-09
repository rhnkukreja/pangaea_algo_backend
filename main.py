import uvicorn
import os
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.agreement import router as agreement_router
from fastapi.responses import PlainTextResponse
from api.portfolio import router as portfolio_router
from auth.auth_supabase import router as auth_router
from api.onboarding import router as onboarding_router
from api.referral import router as referral_router
from api.matching import router as matching_router
from matching_api import router as matching_v2_router
from pangaea_demo_router import router as demo_router

logger = logging.getLogger("pangaea")

app = FastAPI(title="Developer Onboarding API")
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error("422 Validation error on %s %s → %s", request.method, request.url.path, exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method in ("POST", "PUT", "PATCH"):
        body = await request.body()
        logger.info(">>> %s %s  body: %s", request.method, request.url.path, body.decode("utf-8", errors="replace"))
        # Rebuild the body stream so FastAPI can still read it
        async def receive():
            return {"type": "http.request", "body": body}
        request._receive = receive
    return await call_next(request)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agreement_router, prefix="/api", tags=["Agreement"])
app.include_router(portfolio_router,prefix="/api/portfolio",tags=["Portfolio"])
app.include_router(auth_router, prefix="/api", tags=["Auth-Supabase"])
app.include_router(onboarding_router, prefix="/api/onboarding", tags=["developer-onboarding"])
app.include_router(referral_router, prefix="/api/referral", tags=["Referral"])
app.include_router(demo_router, tags=["Demo"])
app.include_router(matching_router, prefix="/api", tags=["Matching"])
app.include_router(matching_v2_router, prefix="/api", tags=["Matching-V2"])

@app.get("/", tags=["Health"])
async def health_check():
    return PlainTextResponse("Welcome to Pangaea Advisory..", status_code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
