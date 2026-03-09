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

Interactive command-line tool for creating and managing geometric shapes.
Built with clean architecture.

</div>

---

## 📋 Table of Contents
- [Features](#features-english)
- [Quick Start](#quick-start-english)
- [Project Structure](#project-structure-english)
- [Usage](#usage-english)
- [Persistent Storage](#persistent-storage-english)
- [Architecture](#architecture-english)
- [Logging System](#logging-system-english)
- [Development](#development-english)
- [License](#license-english)

---

<a id="features-english"></a>
## ✨ Features

- **Shape Management**:
  - Create points, lines, circles, squares, rectangles, ellipses
  - List all shapes with formatted output
  - Delete shapes by ID (with partial ID matching)
  - Clear all shapes at once
  - Count total shapes

- **Persistent Storage**:
  - Save current shapes to a JSON file
  - Load shapes from a JSON file with intelligent merging
  - Automatic conflict resolution (duplicate IDs are skipped)
  - Configurable file location (default: `database/shapes.json`)

- **Clean Architecture**:
  - Strict separation of concerns (Domain, Application, Infrastructure)
  - Repository pattern for data storage
  - Dependency injection ready
  - Interface-based design

- **Enterprise Logging**:
  - Structured logging with `structlog`
  - JSON output for production, colored console for development
  - Context binding
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
├── database/                            # Persistent storage (JSON files)
│   └── shapes.json                      # Default shape file
├── logs/                                # Application logs
├── src/
│   └── vector_editor/
│       ├── application/                 # Application layer
│       │   └── services/                # ShapeService (use cases)
│       ├── cli/                         # CLI interface
│       │   ├── app.py                   # Click commands
│       │   └── formatting.py            # Console output
│       ├── config/                      # Configuration
│       │   └── config.py                # Pydantic settings
│       ├── domain/                      # Core business logic
│       │   ├── definitions/             # Shape definitions
│       │   ├── geometry/                # Geometric representations
│       │   ├── interfaces/              # Repository protocol
│       │   ├── primitives/              # Coordinates, Transform
│       │   └── placed_shape.py          # Shape with ID & transform
│       ├── infrastructure/              # External concerns
│       │   ├── repositories/            # InMemoryShapeRepository
│       │   └── serialization.py         # JSON serialization
│       ├── logger/                      # Structured logging system
│       └── utils/                       # Helpers (Singleton)
├── tests/                               # Unit tests
├── main.py                              # Entry point
├── pyproject.toml                       # Project configuration
├── docker-compose.yml                   # Docker setup
└── Makefile                             # Development tasks
```

---

<a id="usage-english"></a>
## 🎯 Usage

### Interactive Commands

| Command | Description | Example |
|---------|-------------|---------|
| `point <x> <y> [--angle <degrees>]` | Create a point | `point 10.5 -20 --angle 45` |
| `line <start_x> <start_y> <end_x> <end_y> [--angle <degrees>]` | Create a line from coordinates | `line 0 0 10 10` |
| `line-polar <start_x> <start_y> <length> <angle_degrees> [--angle <additional_degrees>]` | Create a line by polar method | `line 0 0 10 60` |
| `circle <center_x> <center_y> <radius> [--angle <degrees>]` | Create a circle | `circle 5 -5 3` |
| `square <center_x> <center_y> <side_size> [--angle <degrees>]` | Create a square | `square 1 1 4 -a 45` |
| `rectangle <center_x> <center_y> <width> <height> [--angle <degrees>]` | Create a rectangle | `rectangle 2 3 4 5` |
| `ellipse <center_x> <center_y> <radius_x> <radius_y> [--angle <degrees>]"` | Create an ellipse | `ellipse 3 4 2 3` |
| `list` | List all shapes | `list` |
| `delete <id>` | Delete shape by ID | `delete 123e4567` |
| `clear` | Delete all shapes | `clear` |
| `count` | Show total shapes | `count` |
| `save [<filename>]` | Save shapes to file | `save my_shapes.json` |
| `load [<filename>]` | Load shapes from file | `load my_shapes.json` |
| `help [command]` | Show help | `help circle` |
| `q`, `quit`, `exit` | Exit CLI | `q` |

---

<a id="persistent-storage-english"></a>
## 💾 Persistent Storage

### Saving Shapes
- `save` without argument saves to `database/shapes.json`.
- If the file already exists, you will be prompted:
  - **Append** – loads existing shapes, merges with current (duplicate IDs are skipped), and saves combined set.
  - **Overwrite** – replaces file content with current shapes.

### Loading Shapes
- `load` without argument loads from `database/shapes.json`.
- If there are shapes already in memory:
  - **Add** – adds loaded shapes, skipping duplicates.
  - **Replace** – clears memory and loads shapes from file.

This design ensures you never lose data unintentionally and have full control over merging.

---

<a id="architecture-english"></a>
## 🏗 Architecture

1. **Domain Layer**: Pure Python with dataclasses, no external dependencies.
2. **Repository Pattern**: Abstract `IShapeRepository` protocol enables easy swapping of storage (in‑memory, file‑based, etc.).
3. **Serialization**: Infrastructure module converts domain objects to/from JSON.
4. **Dependency Injection**: Services receive repository and config via constructor.
5. **Protocol-based Interfaces**: Uses `typing.Protocol` for loose coupling.

---

<a id="logging-system-english"></a>
## 📝 Logging System

A sophisticated, production-ready logging system built with `structlog`.

### Features

- **Structured Logging**: All logs are structured events, not just strings.
- **Dual Output**:
  - Development: Beautiful colored console output.
  - Production: JSON format for log aggregation.
- **File Rotation**: Built-in log rotation with size limits.
- **Third-party Hijacking**: Automatically configures logs for `pydantic`.

### Configuration

Via `config.py` or `.env`(optional):

```python
LoggingConfig(
    debug=True,                          # False for JSON output
    app_name="Vector Editor",
    log_level="INFO",
    enable_file_logging=False,
)
FileSystem(
    db_dir=Path("database"),
    db_json_file_name="shapes.json",
    logs_dir=Path("logs"),
    logs_file_name="app.log",
    max_log_file_size_mb=10,
    log_backup_count=5,
)
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

# Install pre-commit hooks
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

- **ruff**: Fast Python linter and formatter (line length 79).
- **ty**: Fast type checking.
- **pytest**: Comprehensive test suite with coverage.
- **pre-commit**: Automated checks before commits.

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

MIT License – free to use and modify.


<br>
<hr>
<br>

<a id="russian"></a>

<div align="center">
  <a href="#english">🇬🇧 English</a> | <a href="#russian">🇷🇺 Русский</a>
</div>
<br>

---

<a id="russian"></a>
<div align="center">

# 📐 Редактор векторных фигур (CLI)

Интерактивный инструмент командной строки для создания и управления геометрическими фигурами.
Построен на принципах чистой архитектуры.

</div>

---

## 📋 Содержание
- [Возможности](#возможности-russian)
- [Быстрый старт](#быстрый-старт-russian)
- [Структура проекта](#структура-проекта-russian)
- [Использование](#использование-russian)
- [Постоянное хранилище](#постоянное-хранилище-russian)
- [Архитектура](#архитектура-russian)
- [Система логирования](#система-логирования-russian)
- [Разработка](#разработка-russian)
- [Лицензия](#лицензия-russian)

---

<a id="возможности-russian"></a>
## ✨ Возможности

- **Управление фигурами**:
  - Создание точек, линий, кругов, квадратов, прямоугольников, эллипсов
  - Просмотр всех фигур с форматированным выводом
  - Удаление фигур по ID (с поддержкой частичного совпадения)
  - Удаление всех фигур одной командой
  - Подсчёт общего количества фигур

- **Постоянное хранилище**:
  - Сохранение текущих фигур в JSON-файл
  - Загрузка фигур из JSON-файла с опциональным слиянием
  - Автоматическое разрешение конфликтов (дублирующиеся ID пропускаются)
  - Настраиваемое расположение файла (по умолчанию: `database/shapes.json`)

- **Чистая архитектура**:
  - Чёткое разделение слоёв (домен, приложение, инфраструктура)
  - Паттерн «Репозиторий» для хранения данных
  - Готовность к внедрению зависимостей
  - Проектирование на основе интерфейсов

- **Промышленное логирование**:
  - Структурированное логирование с помощью `structlog`
  - Вывод в JSON для продакшена, цветной вывод для разработки
  - Привязка контекста
  - Поддержка ротации файлов
  - Перехват логов сторонних библиотек

- **Готовность к продакшену**:
  - Полная типизация (Python 3.14)
  - Линтинг и форматирование с Ruff
  - Pre-commit хуки для контроля качества кода
  - Поддержка Docker с `uv` для быстрой сборки
  - Комплексный набор тестов

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

# Установка с помощью uv
uv venv
uv pip install -e .
```

### Запуск CLI

```bash
# Запуск интерактивного CLI
uv run python main.py

# С использованием Docker
docker-compose up

# С использованием Makefile
make run
```

---

<a id="структура-проекта-russian"></a>
## 📁 Структура проекта

```
├── database/                            # Постоянное хранилище (JSON-файлы)
│   └── shapes.json                      # Файл хранения по умолчанию
├── logs/                                # Логи приложения
├── src/
│   └── vector_editor/
│       ├── application/                 # Слой приложения
│       │   └── services/                # ShapeService
│       ├── cli/                         # Интерфейс командной строки
│       │   ├── app.py                   # Команды Click
│       │   └── formatting.py            # Вывод в консоль
│       ├── config/                      # Конфигурация
│       │   └── config.py                # Настройки Pydantic
│       ├── domain/                      # Основная бизнес-логика
│       │   ├── definitions/             # Определения фигур
│       │   ├── geometry/                # Геометрические представления
│       │   ├── interfaces/              # Протокол репозитория
│       │   ├── primitives/              # Координаты, трансформация
│       │   └── placed_shape.py          # Фигура с ID и трансформацией
│       ├── infrastructure/              # Внешние зависимости
│       │   ├── repositories/            # InMemoryShapeRepository
│       │   └── serialization.py         # JSON-сериализация
│       ├── logger/                      # Система структурированного логирования
│       └── utils/                       # Вспомогательные утилиты (Singleton)
├── tests/                               # Модульные тесты
├── main.py                              # Точка входа
├── pyproject.toml                       # Метаданные проекта
├── docker-compose.yml                   # Настройки Docker
└── Makefile                             # Задачи разработки
```

---

<a id="использование-russian"></a>
## 🎯 Использование

### Интерактивные команды

| Команда | Описание | Пример |
|---------|----------|---------|
| `point <x> <y> [--angle <degrees>]` | Создать точку | `point 10.5 -20 --angle 45` |
| `line <start_x> <start_y> <end_x> <end_y> [--angle <degrees>]` | Создать линию по координатам | `line 0 0 10 10` |
| `line-polar <start_x> <start_y> <length> <angle_degrees> [--angle <additional_degrees>]` | Создать линию полярным методом | `line 0 0 10 60` |
| `circle <center_x> <center_y> <radius> [--angle <degrees>]` | Создать круг | `circle 5 -5 3` |
| `square <center_x> <center_y> <side_size> [--angle <degrees>]` | Создать квадрат | `square 1 1 4 -a 45` |
| `rectangle <center_x> <center_y> <width> <height> [--angle <degrees>]` | Создать прямоугольник | `rectangle 2 3 4 5` |
| `ellipse <center_x> <center_y> <radius_x> <radius_y> [--angle <degrees>]"` | Создать эллипс | `ellipse 3 4 2 3` |
| `list` | Показать все фигуры | `list` |
| `delete <id>` | Удалить фигуру по ID | `delete 123e4567` |
| `clear` | Удалить все фигуры | `clear` |
| `count` | Показать общее количество фигур | `count` |
| `save [<filename>]` | Сохранить фигуры в файл | `save my_shapes.json` |
| `load [<filename>]` | Загрузить фигуры из файла | `load my_shapes.json` |
| `help [command]` | Показать справку | `help circle` |
| `q`, `quit`, `exit` | Выйти из CLI | `q` |

---

<a id="постоянное-хранилище-russian"></a>
## 💾 Постоянное хранилище

### Сохранение фигур
- `save` без аргумента сохраняет в `database/shapes.json`.
- Если файл уже существует, будет задан вопрос:
  - **Добавить** – загружает существующие фигуры, объединяет с текущими (дублирующиеся ID пропускаются) и сохраняет объединённый набор.
  - **Перезаписать** – заменяет содержимое файла текущими фигурами.

### Загрузка фигур
- `load` без аргумента загружает из `database/shapes.json`.
- Если в памяти уже есть фигуры:
  - **Добавить** – добавляет загруженные фигуры, пропуская дубликаты.
  - **Заменить** – очищает память и загружает фигуры из файла.

Такое поведение гарантирует, что вы никогда не потеряете данные случайно и сохраняете полный контроль над слиянием.

---

<a id="архитектура-russian"></a>
## 🏗 Архитектура

1. **Слой домена**: Чистый Python с датаклассами, без внешних зависимостей.
2. **Паттерн «Репозиторий»**: Абстрактный протокол `IShapeRepository` позволяет легко заменять хранилище (в памяти, на основе файлов и т.д.).
3. **Сериализация**: Модуль инфраструктуры преобразует объекты домена в JSON и обратно.
4. **Внедрение зависимостей**: Сервисы получают репозиторий и конфигурацию через конструктор.
5. **Интерфейсы на основе протоколов**: Использование `typing.Protocol` для слабой связанности.

---

<a id="система-логирования-russian"></a>
## 📝 Система логирования

Сложная, готовая к продакшену система логирования на базе `structlog`.

### Возможности

- **Структурированное логирование**: Все логи — это структурированные события, а не просто строки.
- **Два режима вывода**:
  - Разработка: красивый цветной вывод в консоль.
  - Продакшен: JSON-формат для агрегации логов.
- **Ротация файлов**: Встроенная ротация логов с ограничением по размеру.
- **Перехват сторонних логгеров**: Автоматически настраивает логи для `pydantic`.

### Конфигурация

Через `config.py` или `.env` (опционально):

```python
LoggingConfig(
    debug=True,                          # False для JSON-вывода
    app_name="Vector Editor",
    log_level="INFO",
    enable_file_logging=False,
)
FileSystem(
    db_dir=Path("database"),
    db_json_file_name="shapes.json",
    logs_dir=Path("logs"),
    logs_file_name="app.log",
    max_log_file_size_mb=10,
    log_backup_count=5,
)
```

---

<a id="разработка-russian"></a>
## 🛠 Разработка

### Настройка

```bash
# Установка с dev-зависимостями
uv pip install -e . --group dev

# Активировать виртуальное окружение
source .venv/bin/activate  # или .venv\Scripts\activate

# Установить pre-commit хуки
pre-commit install

# Запустить тесты
make test

# Запустить линтер
make lint

# Исправить форматирование
make fix

# Очистить кеш
make clean
```

### Качество кода

- **ruff**: Быстрый линтер и форматтер Python (длина строки 79).
- **ty**: Быстрая проверка типов.
- **pytest**: Комплексный набор тестов с покрытием.
- **pre-commit**: Автоматические проверки перед коммитами.

### Docker

```bash
# Собрать и запустить
make docker-run

# Пересобрать
make docker-rebuild

# Или вручную
docker-compose run --rm vector-editor
docker-compose down
```

### Тестирование

```bash
# Запустить все тесты
uv run pytest

# С отчётом о покрытии
uv run pytest --cov=src --cov-report=html

# Конкретный тест
uv run pytest tests/unit/cli/test_cli.py
```

---

<a id="лицензия-russian"></a>
## 📝 Лицензия

Лицензия MIT – можно свободно использовать и модифицировать.

---
