import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.agreement import router as agreement_router
from fastapi.responses import PlainTextResponse
from api.portfolio import router as portfolio_router
from auth.auth_supabase import router as auth_router
from api.onboarding import router as onboarding_router
from api.referral import router as referral_router

app = FastAPI(title="Developer Onboarding API")

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

@app.get("/", tags=["Health"])
async def health_check():
    return PlainTextResponse("Welcome to Pangaea Advisory..", status_code=200)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
