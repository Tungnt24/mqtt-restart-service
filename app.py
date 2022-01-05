import time
from typing import List
import requests
import subprocess
from settings import Config
from logger import logger


def get_client_offline(url: str, headers: dict) -> List:
    response = requests.request("GET", url, headers=headers)
    data = response.json()
    result = []
    for client in data['table']:
        if not client.get("is_online"):
            result.append(client)
    return result


def restart_service(service_name: str) -> None:
    subprocess.run(["supervisorctl", "restart", service_name])


def main():
    while True:
        clients = get_client_offline(Config.api, Config.headers)
        for client in clients:
            if int(client.get("offline_messages")) > 10:
                service_name = client.get("client_id")
                logger.info("Restart service %s", service_name)
                restart_service(service_name)
        time.sleep(1)


if __name__ == "__main__":
    main()
