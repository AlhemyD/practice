import os
import subprocess
from logger import get_logger

logger=get_logger("crud")

def reformat_crx_to_rnx(crx_file_path: str):
    if not(crx_file_path.endswith(".crx") or crx_file_path.endswith(".24d")):#Проверяю файл на формат (полезно не удалять!)
        logger.error(f"The file is  not a .crx or .24d")
        return {"error": f"file_name '{crx_file_path}' is not a .crx or .24d file"}
    if crx_file_path.endswith(".crx"):
        rnx_file_path = crx_file_path.replace('.crx', '.rnx')
    else:
        rnx_file_path = crx_file_path.replace('.24d', '.rnx')
    file_name_rnx = os.path.basename(os.path.splitext(crx_file_path)[0]) + ".rnx"

    if  os.path.exists(file_name_rnx):#Проверка на существование файла с форматом .rnx
        logger.error(f"Such a file already exists. Formatting is not required.")
        return {"error": "Such a file already exists."}

    if os.path.exists(crx_file_path):
        try:
            subprocess.run(['../lib/RNXCMP_4.1.0_Linux_x86_32bit/bin/CRX2RNX', crx_file_path, '-f'], check=True)
            logger.info(f'{crx_file_path} has been reformatted to {rnx_file_path}')
            return {"file_name": rnx_file_path}
        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting to RNX: {e}")
            return {"error": "Error converting  to RNX"}
    else:
        logger.error(f"The file name '{crx_file_path}' does not exist in this directory")
        return {"error": "The file does not exist."}
