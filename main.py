from fastapi import FastAPI
from api.v1.routes import api_router
from fastapi.middleware.cors import CORSMiddleware
from utils import UnicornException, unicorn_exception_handler

app = FastAPI()
app.add_exception_handler(UnicornException, unicorn_exception_handler)
origins = [
    "http://localhost",
    "http://localhost:9000",
    "http://127.0.0.1:9000",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
