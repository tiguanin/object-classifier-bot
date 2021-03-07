import logging

from src.config import props

LOG_FILE = props['PATHS']['LOG_FILE']

# set up logging to file
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

def getLogger():
    return logging.getLogger('')