"""Fusion package"""
from pathlib import Path
from os import environ
import logging

logging.basicConfig(
    filename="fusor.log",
    format="[%(asctime)s] - %(name)s - %(levelname)s : %(message)s")
logger = logging.getLogger("fusor")
logger.setLevel(logging.DEBUG)


if "SEQREPO_DATA_PATH" in environ:
    SEQREPO_DATA_PATH = environ["SEQREPO_DATA_PATH"]
else:
    SEQREPO_DATA_PATH = "/usr/local/share/seqrepo/latest"

if "UTA_DB_URL" in environ:
    UTA_DB_URL = environ["UTA_DB_URL"]
else:
    UTA_DB_URL = "postgresql://uta_admin@localhost:5433/uta/uta_20210129"

from fusor.fusor import FUSOR  # noqa: E402, F401

APP_ROOT = Path(__file__).resolve().parents[0]
