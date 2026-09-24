import requests
import time
from datetime import datetime, timezone
from dataclasses import dataclass
from database import store_result
import mini_downdetector_logger
import logging 
import uuid

logger = logging.getLogger("mini-downdetector.main")

@dataclass
class MonitorResult:
    url : str
    status_code: int | None
    response_time: float | None
    check_datetime: datetime
    error: str | None
    txid: str  


def check_url(url, txid):
    t_0 = time.perf_counter()
    check_datetime = datetime.now(timezone.utc).replace(microsecond=0)
    try: 
        logger.info('Attempting HTTP request', extra={"url": url, "txid": txid})
        r = requests.get(url, timeout=3)
    except requests.ConnectionError as conn_err:
        logger.error('Connection error during HTTP Request', extra={"url": url, "txid": txid, "error": conn_err})
        return MonitorResult(url=url, status_code=None, response_time=None, check_datetime=check_datetime, error="connection_error", txid=txid)
    except requests.ConnectTimeout as conn_timeout:
        logger.error('Timeout error during HTTP Request', extra={"url": url, "txid": txid, "error": conn_timeout})
        return MonitorResult(url=url, status_code=None, response_time=None, check_datetime=check_datetime, error="timeout", txid=txid)
    t_1 = time.perf_counter()
    response_time = round(t_1 - t_0, 2)
    logger.info('HTTP request succeeded', extra={"url": url, "status_code":r.status_code, "response_time": response_time, "txid": txid})
    return MonitorResult(url, r.status_code, response_time, check_datetime, None, txid)

def main():

    monitored_urls = [
    "https://facebook.com",
    "https://youtube.com",
    "https://linkedin.com",
    "https://badhttp.dev/flaky/50"
    ]

    for url in monitored_urls:
        txid = str(uuid.uuid4())
        logger.info(f'Starting monitoring', extra={"url": url, "txid": txid})
        response = check_url(url,txid)
        store_result(response,txid)

if __name__ == "__main__":
    main()