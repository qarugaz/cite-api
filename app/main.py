from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import writer, article

app = FastAPI(title="Research Writing Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(writer.router, tags=["writer"])
app.include_router(article.router, tags=["article"])

@app.get("/")
def read_root():
    return {"message": "Academic Research and Writing Assistant API"}
