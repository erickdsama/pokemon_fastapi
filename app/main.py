from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from pokemon.infrastructure.router import tour_router

app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(prefix='/v1', router=tour_router, dependencies=[])

