import logging

from utils.config import props

LOG_FILE = props["PATHS"]["LOG_FILE"]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
    datefmt="%m-%d %H:%M",
    filename=LOG_FILE,
    filemode="w",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)


def get_logger():
    return logging.getLogger("")
