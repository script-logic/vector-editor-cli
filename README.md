<div align="center">

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/release/python-314/) [![Click](https://img.shields.io/badge/click-8.1-blue)](https://click.palletsprojects.com/) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Type checked: ty](https://img.shields.io/badge/types-ty-blue)](https://github.com/astral-sh/ty) [![Docker](https://img.shields.io/badge/docker-ready-2496ED)](https://www.docker.com/) [![Pydantic](https://img.shields.io/badge/pydantic-v2-red)](https://docs.pydantic.dev/) [![Structlog](https://img.shields.io/badge/structlog-25.0-lightgrey)](https://www.structlog.org/) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen)](https://pre-commit.com/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)

</div>

<div align="center">
  <a href="#english">🇬🇧 English</a> | <a href="#russian">🇷🇺 Русский</a>
</div>
<br>

---

<a id="english"></a>
<div align="center">

# 📐 Vector Editor CLI

A clean, interactive command-line tool for creating and managing geometric shapes.
Built with clean architecture.

</div>

---

## 📋 Table of Contents
- [Features](#features-english)
- [Quick Start](#quick-start-english)
- [Project Structure](#project-structure-english)
- [Usage](#usage-english)
- [Architecture](#architecture-english)
- [Logging System](#logging-system-english)
- [Development](#development-english)
- [License](#license-english)

---

<a id="features-english"></a>
## ✨ Features

- **Shape Management**:
  - Create points, lines, circles, and squares
  - List all shapes with formatted output
  - Delete shapes by ID (with partial ID matching)
  - Clear all shapes at once
  - Count total shapes

- **Clean Architecture**:
  - Strict separation of concerns (Domain, Application, Infrastructure)
  - Repository pattern for data storage
  - Dependency injection ready
  - Interface-based design

- **Enterprise Logging**:
  - Structured logging with `structlog`
  - JSON output for production, colored console for development
  - Automatic context binding
  - File rotation support
  - Third-party logger hijacking

- **Production Ready**:
  - Full type hints with Python 3.14
  - Ruff for linting and formatting
  - Pre-commit hooks for code quality
  - Docker support with `uv` for fast builds
  - Comprehensive test suite

---

<a id="quick-start-english"></a>
## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- [uv](https://github.com/astral-sh/uv)
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/script-logic/vector-editor-cli.git
cd vector-editor-cli

# Install with uv
uv venv
uv pip install -e .
```

### Run the CLI

```bash
# Start interactive CLI
uv run python main.py

# Using Docker
docker-compose up

# Using Makefile
make run
```

---

<a id="project-structure-english"></a>
## 📁 Project Structure

```
├── src/
│   └── vector_editor/
│       ├── domain/                      # Core business logic
│       │   ├── entities/                # Shapes (Point, Line, Circle, Square)
│       │   └── interfaces/              # Repository protocol
│       ├── application/                 # Application layer
│       │   └── services/                # ShapeService (use cases)
│       ├── infrastructure/              # External concerns
│       │   └── repositories/            # InMemoryShapeRepository
│       ├── cli/                         # CLI interface
│       │   ├── app.py                   # Click commands
│       │   └── formatting.py            # Console output formatting
│       ├── config/                      # Configuration
│       │   └── config.py                # Pydantic settings
│       ├── logger/                      # Structured logging system
│       │   ├── processors.py            # Log processors
│       │   ├── handlers.py              # File/console handlers
│       │   ├── renderers.py             # JSON/console renderers
│       │   └── manager.py               # Logger configuration
│       └── utils/                       # Helpers
│           └── metaclasses.py           # Singleton pattern
├── tests/                               # Unit tests
├── logs/                                # Application logs (when enabled)
├── main.py                              # Entry point
├── pyproject.toml                       # Project configuration
├── docker-compose.yml                   # Docker setup
└── Makefile                             # Development tasks
```

---

<a id="usage-english"></a>
## 🎯 Usage

### Interactive Commands

Once inside the CLI, you can use the following commands:

| Command | Description | Example |
|---------|-------------|---------|
| `point <x> <y>` | Create a point | `point 10.5 -20` |
| `line <x1> <y1> <x2> <y2>` | Create a line | `line 0 0 10 10` |
| `circle <x> <y> <radius>` | Create a circle | `circle 5 -5 3` |
| `square <x> <y> <side>` | Create a square | `square 1 1 4` |
| `list` | List all shapes | `list` |
| `delete <id>` | Delete shape by ID | `delete 123e4567` |
| `clear` | Delete all shapes | `clear` |
| `count` | Show total shapes | `count` |
| `help [command]` | Show help | `help circle` |
| `q`, `quit`, `exit` | Exit CLI | `q` |

### Features

- **Partial ID Matching**: Delete shapes using just the first 8 characters
- **Input Validation**: Automatic type checking and validation
- **Formatted Output**: Color-coded and well-structured shape display
- **Persistent Logging**: Optional file logging with rotation

---

<a id="architecture-english"></a>
## 🏗 Architecture

1. **Domain Layer**: Pure Python with dataclasses, no external dependencies
2. **Repository Pattern**: Abstract `IShapeRepository` protocol enables easy swapping of storage
3. **Dependency Injection**: Services receive repositories via constructor
4. **Protocol-based Interfaces**: Uses `typing.Protocol` for loose coupling

---

<a id="logging-system-english"></a>
## 📝 Logging System

A sophisticated, production-ready logging system built with `structlog`.

### Features

- **Structured Logging**: All logs are structured events, not just strings
- **Dual Output**:
  - Development: Beautiful colored console output
  - Production: JSON format for log aggregation
- **File Rotation**: Built-in log rotation with size limits
- **Third-party Hijacking**: Automatically configures logs for:
  - `pydantic` (set to INFO level)
- **Singleton Manager**: Ensures single configuration point

### Configuration

Via `config.py` or `.env`(optional):

```python
# Example logging configuration
LoggingConfig(
    debug=True,                          # False for JSON output
    app_name="Vector Editor",
    log_level="INFO",
    enable_file_logging=True,
    logs_dir=Path("logs"),
    logs_file_name="app.log",
    max_file_size_mb=10,
    backup_count=5,
)
```

### Example Log Output

**Development (Console):**
```
2026-03-07 10:30:45 [info     ] application_started      config={'debug': True, ...}
2026-03-07 10:30:47 [debug    ] point_created            shape_id='123e4567' x=10.5 y=20.0
2026-03-07 10:30:49 [debug    ] shapes_retrieved         count=5
```

**Production (JSON):**
```json
{"event": "application_started", "timestamp": "2026-03-07T10:30:45Z", "level": "info", "logger": "main.py", "config": {...}}
{"event": "point_created", "shape_id": "123e4567", "x": 10.5, "y": 20.0, "timestamp": "...", "level": "debug"}
```

---

<a id="development-english"></a>
## 🛠 Development

### Setup

```bash
# Install with dev dependencies
uv pip install -e . --group dev

# Activate venv
source .venv/bin/activate  # or .venv\Scripts\activate

# Install pre-commit hooks (only if venv is activated)
pre-commit install

# Run tests
make test

# Run linter
make lint

# Fix formatting
make fix

# Clean cache
make clean
```

### Code Quality

- **ruff**: Fast Python linter and formatter (line length 79)
- **ty**: Fast type checking
- **pytest**: Comprehensive test suite with coverage
- **pre-commit**: Automated checks before commits

### Docker

```bash
# Build and run
make docker-run

# Rebuild
make docker-rebuild

# Or manually
docker-compose run --rm vector-editor
docker-compose down
```

### Testing

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=src --cov-report=html

# Specific test
uv run pytest tests/unit/cli/test_cli.py
```

---

<a id="license-english"></a>
## 📝 License

MIT License - feel free to use and modify.

---

<br>
<hr>
<br>

<a id="russian"></a>

<div align="center">
  <a href="#english">🇬🇧 English</a> | <a href="#russian">🇷🇺 Русский</a>
</div>

<div align="center">

# 📐 Редактор Векторных Фигур (CLI)

Интерактивный инструмент командной строки для создания и управления геометрическими фигурами.
Построен на принципах чистой архитектуры.

</div>

---

## 📋 Содержание
- [Возможности](#возможности-russian)
- [Быстрый старт](#быстрый-старт-russian)
- [Структура проекта](#структура-проекта-russian)
- [Использование](#использование-russian)
- [Архитектура](#архитектура-russian)
- [Система логирования](#система-логирования-russian)
- [Разработка](#разработка-russian)
- [Лицензия](#лицензия-russian)

---

<a id="возможности-russian"></a>
## ✨ Возможности

- **Управление фигурами**:
  - Создание точек, линий, кругов и квадратов
  - Просмотр всех фигур с форматированием
  - Удаление по ID (с поддержкой частичного совпадения)
  - Удаление всех фигур одной командой
  - Подсчёт количества фигур

- **Чистая архитектура**:
  - Чёткое разделение слоёв (Domain, Application, Infrastructure)
  - Паттерн Repository для хранения данных
  - Dependency injection
  - Интерфейсы через Protocol

- **Промышленное логирование**:
  - Структурированные логи через `structlog`
  - JSON для продакшена, цветной вывод для разработки
  - Автоматический контекст
  - Ротация файлов
  - Конфигурация сторонних логгеров

- **Готов к продакшену**:
  - Полная типизация (Python 3.14)
  - Линтинг и форматирование Ruff
  - Pre-commit хуки
  - Docker с `uv`
  - Комплексные тесты

---

<a id="быстрый-старт-russian"></a>
## 🚀 Быстрый старт

### Требования
- Python 3.14+
- [uv](https://github.com/astral-sh/uv)
- Docker (опционально)

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/script-logic/vector-editor-cli.git
cd vector-editor-cli

# Установка с uv
uv venv
uv pip install -e .
```

### Запуск CLI

```bash
# Запуск интерактивного CLI
uv run python main.py

# Через Docker
docker-compose up

# Через Makefile
make run
```

---

<a id="структура-проекта-russian"></a>
## 📁 Структура проекта

```
├── src/
│   └── vector_editor/
│       ├── domain/                      # Бизнес-логика
│       │   ├── entities/                # Фигуры (Point, Line, Circle, Square)
│       │   └── interfaces/              # Протокол репозитория
│       ├── application/                 # Слой приложения
│       │   └── services/                # ShapeService (use cases)
│       ├── infrastructure/              # Внешние зависимости
│       │   └── repositories/            # InMemoryShapeRepository
│       ├── cli/                         # Интерфейс командной строки
│       │   ├── app.py                   # Click команды
│       │   └── formatting.py            # Форматирование вывода
│       ├── config/                      # Конфигурация
│       │   └── config.py                # Pydantic настройки
│       ├── logger/                      # Система логирования
│       │   ├── processors.py            # Процессоры логов
│       │   ├── handlers.py              # Обработчики (файл/консоль)
│       │   ├── renderers.py             # Рендереры (JSON/консоль)
│       │   └── manager.py               # Менеджер логгера
│       └── utils/                       # Вспомогательные утилиты
│           └── metaclasses.py           # Паттерн Singleton
├── tests/                               # Модульные тесты
├── logs/                                # Логи приложения (если включено)
├── main.py                              # Точка входа
├── pyproject.toml                       # Конфигурация проекта
├── docker-compose.yml                   # Docker настройки
└── Makefile                             # Задачи разработки
```

---

<a id="использование-russian"></a>
## 🎯 Использование

### Команды

| Команда | Описание | Пример |
|---------|----------|---------|
| `point <x> <y>` | Создать точку | `point 10.5 -20` |
| `line <x1> <y1> <x2> <y2>` | Создать линию | `line 0 0 10 10` |
| `circle <x> <y> <radius>` | Создать круг | `circle 5 -5 3` |
| `square <x> <y> <side>` | Создать квадрат | `square 1 1 4` |
| `list` | Показать все фигуры | `list` |
| `delete <id>` | Удалить фигуру по ID | `delete 123e4567` |
| `clear` | Удалить все фигуры | `clear` |
| `count` | Показать количество | `count` |
| `help [команда]` | Показать справку | `help circle` |
| `q`, `quit`, `exit` | Выход | `q` |

### Особенности

- **Частичный ID**: Удаляйте фигуры по первым 8 символам ID
- **Валидация**: Автоматическая проверка типов и значений
- **Цветной вывод**: Удобное форматирование фигур
- **Логирование**: Опциональное сохранение в файл с ротацией

---

<a id="архитектура-russian"></a>
## 🏗 Архитектура

1. **Слой Domain**: Чистый Python, никаких внешних зависимостей
2. **Паттерн Repository**: Абстрактный протокол `IShapeRepository` для лёгкой замены хранилища
3. **Dependency Injection**: Сервисы получают репозиторий через конструктор
4. **Интерфейсы через Protocol**: Слабая связанность компонентов

---

<a id="система-логирования-russian"></a>
## 📝 Система логирования

Промышленная система логирования на базе `structlog`.

### Возможности

- **Структурированные логи**: Все логи - это события, а не строки
- **Два режима**:
  - Разработка: цветной вывод в консоль
  - Продакшен: JSON для агрегации
- **Ротация**: Встроенная ротация с ограничением по размеру
- **Конфигурация сторонних библиотек**: Автоматически настраивает:
  - `pydantic` (уровень INFO)
- **Singleton**: Единая точка конфигурации

### Конфигурация

Через `config.py` или `.env`(опционально):

```python
# Пример конфигурации логирования
LoggingConfig(
    debug=True,                          # False для JSON вывода
    app_name="Vector Editor",
    log_level="INFO",
    enable_file_logging=True,
    logs_dir=Path("logs"),
    logs_file_name="app.log",
    max_file_size_mb=10,
    backup_count=5,
)
```

### Пример вывода

**Разработка (Консоль):**
```
2026-03-07 10:30:45 [info     ] application_started      config={'debug': True, ...}
2026-03-07 10:30:47 [debug    ] point_created            shape_id='123e4567' x=10.5 y=20.0
2026-03-07 10:30:49 [debug    ] shapes_retrieved         count=5
```

**Продакшен (JSON):**
```json
{"event": "application_started", "timestamp": "2026-03-07T10:30:45Z", "level": "info", "logger": "main.py", "config": {...}}
{"event": "point_created", "shape_id": "123e4567", "x": 10.5, "y": 20.0, "timestamp": "...", "level": "debug"}
```

---

<a id="разработка-russian"></a>
## 🛠 Разработка

### Настройка

```bash
# Установка с dev зависимостями
uv pip install -e . --group dev

# Активировать окружение (если не активно)
source .venv/bin/activate  # или .venv\Scripts\activate

# Установка pre-commit хуков (только с активированным окружением)
pre-commit install

# Запуск тестов
make test

# Линтинг
make lint

# Авто-исправление
make fix

# Очистка кеша
make clean
```

### Качество кода

- **ruff**: Быстрый линтер и форматтер (длина строки 79)
- **ty**: Быстрая проверка типов
- **pytest**: Комплексные тесты с покрытием
- **pre-commit**: Автоматические проверки

### Docker

```bash
# Сборка и запуск
make docker-run

# Пересборка
make docker-rebuild

# Или вручную
docker-compose run --rm vector-editor
docker-compose down
```

### Тестирование

```bash
# Все тесты
uv run pytest

# С coverage отчётом
uv run pytest --cov=src --cov-report=html

# Конкретный тест
uv run pytest tests/unit/cli/test_cli.py
```

---

<a id="лицензия-russian"></a>
## 📝 Лицензия

MIT License - свободно используйте и модифицируйте.

---
