import logging
import sys

headers = logging.getLogger("Headers")
headers.handlers.clear()
headers.setLevel(logging.INFO)

sys_handler = logging.StreamHandler(sys.stdout)
sys_handler.setFormatter(logging.Formatter('Model Checkpoint: %(message)s'))

headers.addHandler(sys_handler)

# create logger with 'spam_application'
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(module)s.%(funcName)s: %(lineno)d] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
    stream=sys.stdout)
