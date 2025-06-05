import logging

def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Ghi log ra stdout
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Tránh add handler trùng lặp
    if not logger.handlers:
        logger.addHandler(handler)

    return logger