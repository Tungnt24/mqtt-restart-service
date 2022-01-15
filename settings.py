from environs import Env

env = Env()
env.read_env()


class Config:
    api = env.str("API")
    headers = env.json("HEADERS")
    delay = env.int("DELAY")
    offline_message = env.int("OFFLINE_MESSAGE")
    publish_services = env.list("PUBLISH_SERVICES") 
    subcribe_services = env.list("SUBCRIBE_SERVICES")
