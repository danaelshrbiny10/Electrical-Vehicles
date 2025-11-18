from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from routing.simulate import router as simulate_router
from routing.battery import router as battery_router
from routing.charging import router as charging_router
from routing.ai import router as ai_router
from helpers.config import get_settings


from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

settings = get_settings()

app = FastAPI(
    title=f"{settings.APP_NAME} ⚡ AI Simulator",
    description="""
EV AI Simulator API

This API simulates electric vehicle battery consumption, charging curves, and AI-based predictions.

**Endpoints include:**
- `/api/ev/simulate` : Simulate a trip with energy/battery prediction
- `/api/ev/battery_status` : Compute battery remaining after a distance
- `/api/ev/charging_curve` : Estimate charging time and SOC curve
- `/api/ev/ai/predict/consumption` : AI/ML-based energy consumption prediction
""",
    version=settings.APP_VERSION,
    contact={
        "name": "Dana Elshrbiny",
        "email": "danaelshrbiny55@gmail.com",
        "url": "https://github.com/danaelshrbiny10/Electrical-Vehicles",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.DEBUG,
)

# Allow CORS for testing from frontend if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(simulate_router, prefix="/api/ev", tags=["Simulation"])
app.include_router(battery_router, prefix="/api/ev", tags=["Battery"])
app.include_router(charging_router, prefix="/api/ev", tags=["Charging"])
app.include_router(ai_router, prefix="/api/ev/ai", tags=["AI/ML"])


@app.get(
    "/",
    summary="Root endpoint",
    description="Check that the EV AI simulator is running.",
)
def root():
    return {"message": f"{settings.APP_NAME} is running. See /docs for API."}


# This will print validation errors to server logs
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Validation error for request:", await request.body())
    print(exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
