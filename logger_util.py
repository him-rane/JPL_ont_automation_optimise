import logging
import colorlog



def setup_logger():
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    consol_formatter=colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%y-%m-%d %H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG':'white',
            'INFO':'green',
            'WARNING':'yellow',
            'ERROR':'red',
            'CRITICAL':'red,bg_white',
        }
    )

    file_formatter=logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt='%y-%m-%d %H:%M:%S',
    )

    consol_handler=logging.StreamHandler()
    consol_handler.setFormatter(consol_formatter)

    file_handler=logging.FileHandler('logs.log')
    file_handler.setFormatter(file_formatter)

    logger.addHandler(consol_handler)
    logger.addHandler(file_handler)

    return logger


logger=setup_logger()

class Logger():
    logging.basicConfig(filename="logs.log", filemode="w", format="%(asctime)s %(name)s -> %(levelname)s: %(message)s")


    @staticmethod
    def log_warning(msg):
        logging.warning(msg)

    @staticmethod
    def log_info(msg):
        logging.info(msg)

    @staticmethod
    def log_error(msg):
        logging.error(msg)

    @staticmethod
    def log_exp(msg):
        logging.exception(msg)