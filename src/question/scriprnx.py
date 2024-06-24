from fastapi import FastAPI
import sys

sys.path.append("../log")
from logger import get_logger

sys.path.append("../data_processing")
from parser import parsing
from formatting import reformat_crx_to_rnx
import os

app = FastAPI()
logger=get_logger("scriprnx")

@app.get("/")
def hello():
    logger.info("The application responds to your requests successfully.")
    return "hello world!"

@app.get("/reformat/{der}/{file_name}")
async def reformat_crx_by_path(der:str, file_name: str):
    path="../../data"
    crx_file_path = os.path.join(path, der, file_name)
    logger.info("The file format change has started: start func (reformat_crx_to_rnx)")
    return reformat_crx_to_rnx(crx_file_path)

@app.get("/parsing/{der}/{file_name}")
async def parsing_file_name(der:str, file_name: str):
    path="../../data"
    rnx_file_path = os.path.join(path, der, file_name)
    logger.info("Starting parsing")
    return parsing(rnx_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
