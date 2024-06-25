import os
import sys
import subprocess
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../log'))
from logger import get_logger

logger=get_logger("formatting")

def reformat_crx_to_rnx(crx_file_path: str):
    if not(crx_file_path.endswith(".crx") or crx_file_path.endswith("d")):#Проверяю файл на формат (полезно не удалять!)
        logger.error(f"The file is  not a .crx or .24d")
        return {"error": f"file_name '{crx_file_path}' is not a .crx or .24d file"}
#    if crx_file_path.endswith(".crx"):
#        rnx_file_path = crx_file_path.replace('.crx', '.rnx')
#    else:
#        rnx_file_path = crx_file_path.replace('.24d', '.rnx')
    file_name_rnx = os.path.basename(os.path.splitext(crx_file_path)[0]) + ".rnx"

    if  os.path.exists(file_name_rnx):#Проверка на существование файла с форматом .rnx
        logger.error(f"Such a file already exists. Formatting is not required.")
        return {"error": "Such a file already exists."}

    if os.path.exists(crx_file_path):
        try:
            subprocess.run(['../../lib/RNXCMP_4.1.0_Linux_x86_32bit/bin/CRX2RNX', crx_file_path, '-f'], check=True)
            subprocess.run(["rm", crx_file_path, '-f'], check=True)
            logger.info(f'{crx_file_path} has been reformatted to {file_name_rnx}')
            return {"file_name": file_name_rnx}
        except subprocess.CalledProcessError as e:
            logger.error(f"Error converting to RNX: {e}")
            return {"error": "Error converting  to RNX"}
    else:
        logger.error(f"The file name '{crx_file_path}' does not exist in this directory")
        return {"error": "The file does not exist."}
