import logging


def create_main_logger() -> logging.Logger:
    logger = logging.getLogger('main_logger')
    logger.setLevel(logging.WARNING)

    fh = logging.FileHandler('secret_data/main_logs.log')
    fh.setLevel(logging.WARNING)

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s --- %(message)s\n\n')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def create_action_logger() -> logging.Logger:
    logger = logging.getLogger('action_logger')
    logger.setLevel(logging.WARNING)

    fh = logging.FileHandler('secret_data/action_logs.log')
    fh.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s\n'
                                  '%(message)s\n\n')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

