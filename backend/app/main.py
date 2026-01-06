from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.db import create_db_and_tables
import core.fetcher as fetcher

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print('hi')
#     create_db_and_tables()
#     yield

# app = FastAPI(lifespan=lifespan)

# app.include_router(db.router)

create_db_and_tables()
fetcher.run()

