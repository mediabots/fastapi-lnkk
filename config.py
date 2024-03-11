from app import _INIT_CONFIG

def get_config():
    import configparser, os, logging
    global _INIT_CONFIG

    if _INIT_CONFIG:
        return _INIT_CONFIG
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        _INIT_CONFIG = config
    except configparser.Error as e:
        logging.error("issue in reading 'config.ini' file.",e.args)
        os.exit(1)
    return config