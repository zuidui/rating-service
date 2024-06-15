import logging
import os


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Add the function name and class name to the log record
        if record.funcName:
            record.funcName = f"{record.funcName}()"
        else:
            record.funcName = ""

        if "self" in record.__dict__:
            record.className = record.__dict__["self"].__class__.__name__
        else:
            record.className = ""

        return super().format(record)


def logger_config(module: str) -> logging.Logger:
    """
    LOGGER function. Extends Python logging module and sets a custom config.
    params: Module name to __name__ magic method.
    return: Logger object
    usage: logger_config(__name__)
    """
    formatter = CustomFormatter(
        "%(asctime)s[%(levelname)s][%(module)s.%(funcName)s][%(message)s]"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(module)
    logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))

    # Avoid adding multiple handlers
    if not logger.hasHandlers():
        logger.addHandler(handler)

    # Suppress logging from other libraries
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)

    # Optional: Adjust specific SQLAlchemy logger if needed
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)

    return logger


# Set up the root logger
root_logger = logging.getLogger()
root_logger.setLevel(
    logging.WARNING
)  # Set higher level to ignore other libraries' logs

# Avoid adding multiple handlers to the root logger
if not root_logger.hasHandlers():
    root_logger.addHandler(
        logging.StreamHandler()
    )  # Add a handler if not already added

# Apply custom formatting to root logger handlers
for handler in root_logger.handlers:
    handler.setFormatter(
        CustomFormatter(
            "%(asctime)s[%(levelname)s][%(module)s.%(funcName)s][%(message)s]"
        )
    )
