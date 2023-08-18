from loguru import logger

def setup_logger():
    logger.add("./logs/error_log.log", level="ERROR", rotation="100 MB")
    logger.add("./logs/info_log.log", level="INFO", rotation="100 MB")
    logger.add("./logs/trace_log.log", level="TRACE", rotation="100 MB")