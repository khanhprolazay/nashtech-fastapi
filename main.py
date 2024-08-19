from fastapi import FastAPI
from database import DBSession
from routers import user, company, auth, task

app = FastAPI()
app.include_router(user.router)
app.include_router(company.router)
app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
async def helth_check():
    return "OK"

# Initialize the database session for each request
# All route and service function in lower layer will inject the db session to iteract with the database
@app.middleware("http")
async def db_middleware(request, call_next):
    with DBSession() as db:
        request.state.db = db
        response = await call_next(request)
        return response