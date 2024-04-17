from configparser import ConfigParser
from pathlib import Path

if __name__ == "__main__":
    current_folder = Path(__file__).parent.resolve()
    config = ConfigParser()

    config["FOREXLIVE"] = {
        "username": "manhhung.dt6@gmail.com",
        "password": "Blockch@in91",
    }

    with open(f"{current_folder}/accounts.ini", "a") as f:
        config.write(f)