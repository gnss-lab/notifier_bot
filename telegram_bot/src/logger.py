from loguru import logger

def setup_logger():
    logger.add("./telegram_bot/logs/info_log.log", level="INFO", rotation="100 MB")
    logger.add("./telegram_bot/logs/trace_log.log", level="TRACE", rotation="100 MB")