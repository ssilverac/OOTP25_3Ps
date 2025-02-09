import logging

#Logging config

def get_logger(name, file_name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(file_name, mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    if not logger.handlers:
        logger.addHandler(file_handler)

    return logger



