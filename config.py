import configparser


config = configparser.ConfigParser()

config["Paths"] = {
    "BaseDirectory": "/path/to/base/directory",
    "TargetDirectory": "/path/to/target/directory",
}

config["Server"] = {"Host": "localhost", "Port": "7000"}


def getConfig():
    config.read("config.ini")
    return config


def initConfig():
    with open("config.ini", "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    initConfig()
