import logging
from logging.handlers import RotatingFileHandler
import structlog

def configure_logging(log_dir):
    """
    Configure application-wide structured logging.
    Logs go to rotating file AND can be reused everywhere.
    """

    log_file = log_dir / "app.log"

    handler = RotatingFileHandler(
        log_file,
        maxBytes=5_000_000,   # 5 MB
        backupCount=5
    )

    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
