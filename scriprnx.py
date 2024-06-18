from fastapi import FastAPI
import os
from logger import get_logger

app = FastAPI()
logger=get_logger("scriprnx")

def reformat_crx_to_rnx(crx_file_path):
    if not crx_file_path.endswith(".crx"):#Проверяю файл на формат (полезно не удалять!)
        logger.error(f"The {crx_file_path} does not have the .crx format")
        return {"Error" : f"Name file '{crx_file_path}' not a .crx file"}

    file_name_rnx = os.path.basename(os.path.splitext(crx_file_path)[0]) + ".rnx"
    
    if  os.path.exists(file_name_rnx):#Проверка на существование файла с форматом .rnx
        logger.error(f"Such a file already exists. Formatting is not required.")
        return {"Error": "Such a file already exists."}
    
    if os.path.exists(crx_file_path):#Проверяю существует ли файл в директории
        logger.info(f"The beginning of the format change.")
        rnx_file_path = crx_file_path.replace('.crx', '.rnx')
    else:
        logger.error(f"The file name '{crx_file_path}' does not exist in this directory")
        return {"Error": "The file does not exist."}

    with open(crx_file_path, 'rb') as crx_file, open(rnx_file_path, 'wb') as rnx_file:#преобразовывается содерживое файла в нужный формат
        rnx_file.write(crx_file.read())

    logger.info(f'{crx_file_path} has been reformatted to {rnx_file_path}')

    return {"info":"The request has been completed."}

@app.get("/")
def hello():
    logger.info("The application responds to your requests successfully.")
    return "hello world!"

@app.get("/reformat/{crx_file_path}")
async def reformat_crx_by_path(crx_file_path: str):
    logger.info("The file format change has started: start func (reformat_crx_to_rnx)")
    return reformat_crx_to_rnx(crx_file_path)

if __name__ == "__scriprnx__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
