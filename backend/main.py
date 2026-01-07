from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import src.api.live

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(src.api.live.router)

# separate process for fetching
# core server <-- database --> Uvicorn ASGI server <-- FastAPI --> frontend