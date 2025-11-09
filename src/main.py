from fastapi import FastAPI
from controllers import ChargingController, BatteryController, SimulateController

from helpers.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# include routers
app.include_router(SimulateController.router, prefix="/api/ev", tags=["simulate"])
app.include_router(BatteryController.router, prefix="/api/ev", tags=["battery"])
app.include_router(ChargingController.router, prefix="/api/ev", tags=["charging"])


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running. See /docs for API."}
