from random import randint
from configparser import ConfigParser
from pathlib import Path
parent_folder = Path(__file__).parent.resolve().parent
grandparent_folder = parent_folder.parent


def rand_timeout(min: int = 8, max: int = 20) -> int:
    return 100*randint(min, max)


def load_info(user="BABYPIPS") -> dict:
    config = ConfigParser()
    # print(parent_folder)
    config.read(f"{parent_folder}/accounts/accounts.ini")
    try:
        return config[user]
    except:
        print("User not found!")
        exit(0)
