from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import asyncio
import main_bot as bot

# http://127.0.0.1:8000/openapi.json
# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

app = FastAPI()


@app.get("/")
async def root():
    html_content = """
    <html>
    <head>
        <title>My HTML Page</title>
    </head>
    <body>
        <h1>Welcome to FastAPI!</h1>
        <p>Useful links:</p>
        <a href='/docs'>Документация</a><br>
        <a href='/redoc'>Другая документация</a><br>
        <a href='/openapi.json'>Json документация</a><br>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)



@app.get("/test")
async def read_item(num: int, q: str | None = None):
    if q:
        return {"num":num, "q": q}
    return {"num":num}


def start_api():
    print("FastAPI is running...")
    uvicorn.run("fast_api:app", host="0.0.0.0", port=8000, reload=True)

async def main():
    # await asyncio.gather(start_api(), bot.start_bot())
    # await asyncio.gather(start_api())
    task1 = asyncio.create_task(start_api())
    task2 = asyncio.create_task(bot.start_bot())
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())

# os.system("uvicorn fast_api:app --reload")