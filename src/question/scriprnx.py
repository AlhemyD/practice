from fastapi import FastAPI
import sys, os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))

from logger import get_logger
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../data_processing'))
from parser import parsing
from formatting import reformat_crx_to_rnx
from download import download_file_from_url

app = FastAPI()
logger=get_logger("scriprnx")

@app.get("/")
def hello():
    logger.info("Start file download")
    return download_file_from_url()

@app.get("/reformat/{der}/{file_name}")
async def reformat_crx_by_path(der:str, file_name: str):
    path="../../data"
    crx_file_path = os.path.join(path, der, file_name)
    logger.info("The file format change has started: start func (reformat_crx_to_rnx)")
    return reformat_crx_to_rnx(crx_file_path)

@app.get("/parsing/{der}/{file_name}")
async def parsing_file_name(der:str, file_name: str):
    path="../../data"
    if not("/src/practice/" in os.path.dirname(os.path.realpath(__file__))):
        rpath=os.path.dirname(os.path.realpath(__file__))
    else:
        rpath=os.path.join(os.path.dirname(os.path.realpath(__file__)),"../../../src/practice/src/data_processing")
    rnx_file_path = os.path.join(rpath, path, der, file_name)
    logger.info("Starting parsing")
    return parsing(rnx_file_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
