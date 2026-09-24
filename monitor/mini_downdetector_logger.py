import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s %(process)d",
    datefmt="%Y-%m-%dT%H:%M:%SZ"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
