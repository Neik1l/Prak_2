import csv
import os
import sys

# Добавляем src в путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config

def test_config_loading():
    """Тестирование загрузки конфигурации"""
    print("Тестирование загрузки конфигурации...")
    
    # Тест 1: Корректная конфигурация
    print("\n1. Тест корректной конфигурации:")
    try:
        config = Config()
        config.load_from_csv('config.csv')
        config.display_parameters()
        print("✓ Успех")
    except Exception as e:
        print(f"✗ Ошибка: {e}")

def create_test_configs():
    """Создает тестовые конфигурационные файлы для проверки ошибок"""
    test_dir = "test_configs"
    os.makedirs(test_dir, exist_ok=True)
    
    test_cases = [
        # 1. Корректная конфигурация
        ('correct.csv', {
            'package_name': 'test_package',
            'repository_url': 'https://github.com/test/repo',
            'test_mode': 'false',
            'test_repo_path': ''
        }, "Должен работать"),
        
        # 2. Пустое имя пакета
        ('empty_package.csv', {
            'package_name': '',
            'repository_url': 'https://github.com/test/repo',
            'test_mode': 'false',
            'test_repo_path': ''
        }, "Должна быть ошибка - пустое имя пакета"),
        
        # 3. Отсутствует URL в рабочем режиме
        ('no_url.csv', {
            'package_name': 'test_package',
            'repository_url': '',
            'test_mode': 'false',
            'test_repo_path': ''
        }, "Должна быть ошибка - нет URL"),
        
        # 4. Отсутствует путь в тестовом режиме
        ('no_test_path.csv', {
            'package_name': 'test_package',
            'repository_url': '',
            'test_mode': 'true',
            'test_repo_path': ''
        }, "Должна быть ошибка - нет пути в тестовом режиме"),
        
        # 5. Несуществующий файл
        ('nonexistent.csv', None, "Должна быть ошибка - файл не существует")
    ]
    
    for filename, data, description in test_cases:
        filepath = os.path.join(test_dir, filename)
        
        if data is not None:
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=['package_name', 'repository_url', 'test_mode', 'test_repo_path'])
                writer.writeheader()
                writer.writerow(data)
        
        print(f"\nТест: {description}")
        print(f"Файл: {filepath}")
        
        try:
            config = Config()
            config.load_from_csv(filepath)
            config.display_parameters()
            print("Загружено успешно")
        except Exception as e:
            print(f"Ошибка (ожидаемо): {e}")

if __name__ == "__main__":
    print("Создание тестовых конфигураций...")
    create_test_configs()
    print("\nТестирование завершено!")