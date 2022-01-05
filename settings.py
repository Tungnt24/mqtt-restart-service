from environs import Env

env = Env()
env.read_env()


class Config:
    api = env.str("API")
    headers = env.json("HEADERS")
