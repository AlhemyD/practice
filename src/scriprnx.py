from fastapi import FastAPI
import os
from logger import get_logger
from script1 import parsing
import subprocess

app = FastAPI()
logger=get_logger("scriprnx")

def reformat_crx_to_rnx(crx_file_path):
    if not crx_file_path.endswith(".crx"):#Проверяю файл на формат (полезно не удалять!)
        logger.error(f"The does not have the .crx format")
        return {"Error": f"Name file '{crx_file_path}' not a .crx file"}

    rnx_file_path = crx_file_path.replace('.crx', '.rnx')
    file_name_rnx = os.path.basename(os.path.splitext(crx_file_path)[0]) + ".rnx"
    
    if  os.path.exists(file_name_rnx):#Проверка на существование файла с форматом .rnx
        logger.error(f"Such a file already exists. Formatting is not required.")
        return {"Error": "Such a file already exists."}

    if os.path.exists(crx_file_path):
        try:
            logger.info(f'{crx_file_path} has been reformatted to {rnx_file_path}')
            subprocess.run(['RNXCMP_4.1.0_Linux_x86_32bit/bin/CRX2RNX', crx_file_path, '-f'], check=True)
            return {"info": "The request has been completed."}
        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting CRX to RNX: {e}")
            return {"error": "Error converting CRX to RNX"}
    else:
        logger.error(f"The file name '{crx_file_path}' does not exist in this directory")
        return {"Error": "The file does not exist."}

@app.get("/")
def hello():
    logger.info("The application responds to your requests successfully.")
    return "hello world!"

@app.get("/reformat/{crx_file_path}")
async def reformat_crx_by_path(crx_file_path: str):
    logger.info("The file format change has started: start func (reformat_crx_to_rnx)")
    return reformat_crx_to_rnx(crx_file_path)

@app.get("/parsing/{crx_file_path}")
async def parsing_file_name(crx_file_path: str):
    logger.info("parsing")
    return parsing(crx_file_path)


if __name__ == "__scriprnx__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
