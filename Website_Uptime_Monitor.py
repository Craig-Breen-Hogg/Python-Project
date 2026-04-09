import requests
import time

URL = "https://google.com"
INTERVAL = 60

def check_site():
    try:
        response = requests.get(URL, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

if __name__ == "__main__":
    while True:
        status = "UP ✅" if check_site() else "DOWN ❌"
        print(f"{URL} is {status}")
        time.sleep(INTERVAL)
