from gnss_tec import rnx
import os
from logger import get_logger

logger=get_logger("parser")

def parsing(file_name: str):
    if not(file_name.endswith(".rnx") or file_name.endswith(".24o")):
        logger.error(f"File's extension is not correct. file_name: {file_name}")
        return {"error":f"File name not correct - {file_name}"}
    if not(os.path.exists(file_name)):
        logger.error(f"File {file_name} does not exist")
        return {"error":f"File {file_name} does not exist"}
    res={"parse_data":[]}
    with open(file_name) as obs_file:
        reader = rnx(obs_file)
        for tec in reader:
            res["parse_data"].append(
                '{} {}: {} {}'.format(
                    tec.timestamp,
                    tec.satellite,
                    tec.phase_tec,
                    tec.p_range_tec,
                )
            )
    logger.info(f"{file_name} parsing has been completed")
    return res