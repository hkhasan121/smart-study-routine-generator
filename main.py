from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, subjects, routine

app = FastAPI(title="Smart Study Routine Generator")

# 🔓 Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}

app.include_router(auth.router)
app.include_router(subjects.router)
app.include_router(routine.router)
