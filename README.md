# Dependency Visualizer

Инструмент для визуализации графа зависимостей пакетов Rust.

## Этап 1: Минимальный прототип ✅

- Загрузка конфигурации из CSV файла
- Обработка ошибок параметров  
- Вывод параметров в формате ключ-значение

## Этап 2: Сбор данных ✅

- Получение Cargo.toml из GitHub репозиториев
- Парсинг зависимостей из секций [dependencies]
- Вывод прямых зависимостей пакета
- Обработка ошибок сети и парсинга

## Конфигурация

Основной пакет для анализа: **log** (https://github.com/rust-lang/log)

### Формат config.csv:
```csv
package_name,repository_url,test_mode,test_repo_path
log,https://github.com/rust-lang/log,false,