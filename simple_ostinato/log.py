import logging

global _LOGGERS
global _CONSOLE_HANDLER
global _NULL_HANDLER
global _LOG_LEVEL
global _CONSOLE_LOGS

_LOGGERS = []
_CONSOLE_HANDLER = logging.StreamHandler()
_NULL_HANDLER = logging.NullHandler()
_LOG_LEVEL = logging.INFO
_CONSOLE_LOGS = False


def new_logger(name, level='DEBUG'):
    logger = logging.getLogger(name)
    configure_logger(logger)
    _LOGGERS.append(logger)
    return logger


def configure_logger(logger):
    while logger.handlers:
        logger.removeHandler(logger.handlers[-1])
    if _CONSOLE_LOGS:
        logger.addHandler(_CONSOLE_HANDLER)
    else:
        logger.addHandler(_NULL_HANDLER)
    logger.setLevel(_LOG_LEVEL)


def configure_console_logs(formatter=None):
    global _CONSOLE_HANDLER
    if not formatter:
        fmt = '%(asctime)s - %(levelname)8s - %(name)s - %(message)s'
        date_fmt = '%H:%M:%S'
        formatter = logging.Formatter(fmt, date_fmt)
    _CONSOLE_HANDLER.setFormatter(formatter)

configure_console_logs()


def enable_console_logs():
    global _CONSOLE_LOGS
    _CONSOLE_LOGS = True
    for logger in _LOGGERS:
        configure_logger(logger)


def disable_console_logs():
    global _CONSOLE_LOGS
    _CONSOLE_LOGS = False
    for logger in _LOGGERS:
        configure_logger(logger)


def set_log_level(log_level):
    global _LOG_LEVEL
    _LOG_LEVEL = log_level
    _NULL_HANDLER.setLevel(_LOG_LEVEL)
    _CONSOLE_HANDLER.setLevel(_LOG_LEVEL)
    for logger in _LOGGERS:
        configure_logger(logger)
