from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from orm_router import router as organization_router
from auth import get_current_user, AuthBearer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to a list of allowed origins in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow the necessary methods
    allow_headers=["Authorization"],  # Allow the Authorization header
)

# Include the organization router
app.include_router(organization_router, prefix="/api")

@app.get("/upload/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}

@app.get("/protected", dependencies=[Depends(AuthBearer())], tags=["Protected"])
async def protected_route(user = Depends(get_current_user)):
    return user

