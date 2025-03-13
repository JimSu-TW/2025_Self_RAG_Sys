import logging
import os
from datetime import datetime
import sys


class Logger:
    def __init__(self, name, log_level=logging.INFO, log_dir="logs"):
        """
        初始化日誌記錄器

        Args:
            name: 日誌記錄器名稱
            log_level: 日誌級別，預設為 INFO
            log_dir: 日誌檔案目錄，預設為 "logs"
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        self.logger.handlers = []  # 清除任何現有的處理程序

        # 建立日誌目錄
        os.makedirs(log_dir, exist_ok=True)

        # 設定日期格式
        date_format = "%Y-%m-%d_%H-%M-%S"
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # 添加控制台輸出
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        self.logger.addHandler(console_handler)

        # 添加檔案輸出
        current_time = datetime.now().strftime(date_format)
        log_file = os.path.join(log_dir, f"{name}_{current_time}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_format)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


def get_logger(name="rag_system", log_level=logging.INFO, log_dir="logs"):
    """
    獲取日誌記錄器的便捷函數

    Args:
        name: 日誌記錄器名稱
        log_level: 日誌級別
        log_dir: 日誌檔案目錄

    Returns:
        Logger: 設定好的日誌記錄器實例
    """
    return Logger(name, log_level, log_dir)
