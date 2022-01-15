from operator import sub
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


def handle_services(subcribe_services: List[str], publish_services: List[str]) -> None:
    publish_service_names = " ".join(publish_services)
    subcribe_service_names = " ".join(subcribe_services)

    logger.info("Stop services %s", publish_service_names)
    subprocess.run(["supervisorctl", "stop", publish_service_names])

    time.sleep(2)
    logger.info("Restart services %s", subcribe_service_names)
    subprocess.run(["supervisorctl", "restart", subcribe_service_names])

    time.sleep(2)
    logger.info("Start services %s", publish_service_names)
    subprocess.run(["supervisorctl", "start", publish_service_names])


def main():
    while True:
        offline_clients = get_client_offline(Config.api, Config.headers)
        offline_messages = [client.get("offline_messages")
                            for client in offline_clients]

        if sum(offline_messages) >= Config.offline_message:
            subcribe_services = []
            for client in offline_clients:
                client_id = client.get("client_id")
                if client_id in Config.subcribe_services:
                    subcribe_services.append(client_id)
            if not subcribe_services:
                continue
            handle_services(subcribe_services, Config.publish_services)
        time.sleep(Config.delay)


if __name__ == "__main__":
    main()
