"""
Configuration module for the application.

Provides type-safe settings using Pydantic.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.vector_editor.logger import ILoggingConfig


class LoggingConfig(BaseSettings):
    """Configuration for the logging system."""

    app_name: str = "Finance Analysis"
    debug: bool = True  # if True then color console render, else json render
    log_level: str = "INFO"
    enable_file_logging: bool = False


class FileSystem(BaseSettings):
    """Configuration for the file system."""

    db_dir: Path = Path("database")
    db_json_file_name: str = "shapes.json"
    db_json_serialization_version: str = "1.0"
    logs_dir: Path = Path("logs")
    logs_file_name: str = "app.log"
    max_log_file_size_mb: int = 10
    log_backup_count: int = 5


class AppConfig(BaseSettings):
    """Main application configuration."""

    logger: LoggingConfig = Field(default_factory=LoggingConfig)
    file_system: FileSystem = Field(default_factory=FileSystem)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_nested_delimiter="__",
    )

    @property
    def logger_adapter(self) -> ILoggingConfig:
        """
        Create logging configuration adapter from settings.

        Returns:
            ILoggingConfig: Configuration object for the logging system.
        """

        class LoggerAdapter:
            def __init__(self, config: AppConfig):
                self.debug = config.logger.debug
                self.app_name = config.logger.app_name
                self.log_level = config.logger.log_level.upper()
                self.enable_file_logging = config.logger.enable_file_logging
                self.logs_dir = config.file_system.logs_dir
                self.logs_file_name = config.file_system.logs_file_name
                self.max_file_size_mb = config.file_system.max_log_file_size_mb
                self.backup_count = config.file_system.log_backup_count

        return LoggerAdapter(self)


@lru_cache
def get_config() -> AppConfig:
    return AppConfig()
