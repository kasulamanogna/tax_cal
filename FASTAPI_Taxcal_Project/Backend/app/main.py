from fastapi import FastAPI
from .database import Base, engine
from .routes import users, income

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(income.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Tax Calculator API"}


