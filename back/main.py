import time

import uvicorn
from fastapi import FastAPI

from global_config import config, logger
from model import *

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger.info('服务启动')


@app.on_event("shutdown")
async def shutdown_event():
    logger.info('服务关闭')
    time.sleep(config.log_refresh_seconds * 2)
    logger.close_state = True


@app.post("/longin")
async def longin(login_info: Login):
    pass


@app.post("/register")
async def register(register_info: Register):
    pass


@app.get("/download/{username}/{filename}")
async def download_file(username: str, filename: str):
    pass


@app.post("/upload/{username}/{filename}")
async def upload_file(username: str, filename: str):
    pass


@app.post("/upload/{username}/{filename}")
async def query_dir(username: str, filename: str):
    pass


if __name__ == '__main__':
    uvicorn.run(app, host=config.host, port=config.port)
