from fastapi import FastAPI

import src.api.vehicleposition

app = FastAPI()

app.include_router(src.api.vehicleposition.router)

# separate process for fetching
# core server <-- database --> Uvicorn ASGI server <-- FastAPI --> frontend