from fastapi import FastAPI
from logger import get_logger
from script1 import parsing
from models import Path
from crud import reformat_crx_to_rnx

app = FastAPI()
logger=get_logger("scriprnx")

@app.get("/")
def hello():
    logger.info("The application responds to your requests successfully.")
    return "hello world!"

@app.post("/reformat")
async def reformat_crx_by_path(crx_file_path: Path):
    logger.info("The file format change has started: start func (reformat_crx_to_rnx)")
    return reformat_crx_to_rnx(crx_file_path.path)

@app.post("/parsing")
async def parsing_file_name(crx_file_path: Path):
    logger.info("parsing")
    return parsing(crx_file_path.path)


if __name__ == "__scriprnx__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
