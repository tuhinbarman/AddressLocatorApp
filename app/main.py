from fastapi import FastAPI
from database import Base,engine
import models
from routers import address
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key = 'asdf23423kjh23hk23h4kjh23h4kjh23'
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)



app.include_router(address.router,prefix='')