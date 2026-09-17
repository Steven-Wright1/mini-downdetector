import requests
import time
from datetime import datetime, timezone
from dataclasses import dataclass

@dataclass
class MonitorResult:
    url : str
    status_code: int | None
    response_time: float | None
    check_datetime: datetime
    error: str | None


def check_url(url):
    t_0 = time.perf_counter()
    check_datetime = datetime.now(timezone.utc).replace(microsecond=0)
    try: 
        r = requests.get(url, timeout=3)
    except requests.ConnectionError as conn_err:
        # TODO: Add structured logging        
        return MonitorResult(url=url, status_code=None, response_time=None, check_datetime=check_datetime, error="connection_error")
    except requests.ConnectTimeout as conn_timeout:
        # TODO: Add structured logging   
        return MonitorResult(url=url, status_code=None, response_time=None, check_datetime=check_datetime, error="timeout")
    t_1 = time.perf_counter()
    response_time = round(t_1 - t_0, 2)
    return MonitorResult(url, r.status_code, response_time, check_datetime, None)

def main():

    monitored_urls = [
    "https://facebook.com",
    "https://youtube.com",
    "https://linkedin.com",
    "https://badhttp.dev/flaky/50"
    ]

    for url in monitored_urls:
        response = check_url(url)
        print(response)

if __name__ == "__main__":
    main()