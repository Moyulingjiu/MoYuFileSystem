from fastapi import FastAPI
import uvicorn

from global_config import config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/download/{filename}")
async def download_file(filename: str):
    return {"message": f"Hello {filename}"}


if __name__ == '__main__':
    uvicorn.run(app, host=config.host, port=config.port)
