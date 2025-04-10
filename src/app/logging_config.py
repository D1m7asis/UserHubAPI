import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Формат логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)


def setup_logging():
    # Основной логгер приложения
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # Файловый обработчик с ротацией
    log_file_handler = RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )

    log_file_handler.setFormatter(formatter)
    logger.addHandler(log_file_handler)

    return logger


def setup_sql_logger():
    # Логгер SQLAlchemy
    sql_logger = logging.getLogger("sqlalchemy.engine")
    sql_logger.setLevel(logging.INFO)

    # Файловый обработчик с ротацией
    sql_file_handler = RotatingFileHandler(
        filename="logs/sql.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )

    sql_file_handler.setFormatter(formatter)

    sql_logger.addHandler(sql_file_handler)

