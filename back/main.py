import time

import uvicorn
from fastapi import FastAPI

from global_config import config, logger

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info('服务启动')


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('服务关闭')
    time.sleep(config.log_refresh_seconds * 2)
    logger.close_state = True


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/download/{filename}")
async def download_file(filename: str):
    return {"message": f"Hello {filename}"}


if __name__ == '__main__':
    uvicorn.run(app, host=config.host, port=config.port)
