from loguru import logger

# keep default console handler (colored)
logger.add("app.log", format="{time} {level:<8} - {name}:{function} - {message}", level="DEBUG")

def get_logger(name="app"):
    return logger.bind(name=name)
