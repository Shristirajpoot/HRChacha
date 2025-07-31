import logging
import os
from datetime import datetime

from hrchacha.constants import PROJECT_ROOT

LOG_FILE = f"{datetime.now().strftime("%d_%m_%Y_%H:%M:%S")}.log"
logs_path = os.path.join(PROJECT_ROOT, "logs", f"{datetime.now().strftime("%d_%m_%Y_%H:%M")}")
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),
            logging.StreamHandler()
        ],
        format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO

)