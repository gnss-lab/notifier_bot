import os
from fastapi import FastAPI

# http://127.0.0.1:8000/openapi.json
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}



if __name__ == "__main__":
    os.system("uvicorn fast_api:app --reload")
