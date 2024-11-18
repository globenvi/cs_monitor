from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_tokken: str

@dataclass
class Settings:
    bots: Bots


def Config(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_tokken=env.str("BOT_TOKEN"),
        )
    )


config = Config(".env")
