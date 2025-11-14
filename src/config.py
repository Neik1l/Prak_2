import csv
import os
from typing import Dict, Any

class Config:
    def __init__(self):
        self.package_name = ""
        self.repository_url = ""
        self.test_mode = False
        self.test_repo_path = ""
    
    def load_from_csv(self, file_path: str) -> None:
        """Загружает конфигурацию из CSV файла"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Конфигурационный файл не найден: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                
                if not rows:
                    raise ValueError("CSV файл пуст")
                
                # Берем первую строку для конфигурации
                config_row = rows[0]
                
                # Обрабатываем обязательные параметры
                self.package_name = config_row.get('package_name', '').strip()
                if not self.package_name:
                    raise ValueError("Имя пакета не может быть пустым")
                
                self.repository_url = config_row.get('repository_url', '').strip()
                self.test_repo_path = config_row.get('test_repo_path', '').strip()
                
                # Обрабатываем режим работы
                test_mode_str = config_row.get('test_mode', 'false').strip().lower()
                self.test_mode = test_mode_str in ('true', '1', 'yes')
                
                # Валидация параметров
                if self.test_mode and not self.test_repo_path:
                    raise ValueError("В тестовом режиме должен быть указан путь к тестовому репозиторию")
                elif not self.test_mode and not self.repository_url:
                    raise ValueError("В рабочем режиме должен быть указан URL репозитория")
                    
        except csv.Error as e:
            raise ValueError(f"Ошибка чтения CSV файла: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка обработки конфигурации: {e}")
    
    def get_all_parameters(self) -> Dict[str, Any]:
        """Возвращает все параметры в формате ключ-значение"""
        return {
            "package_name": self.package_name,
            "repository_url": self.repository_url,
            "test_mode": self.test_mode,
            "test_repo_path": self.test_repo_path
        }
    
    def display_parameters(self) -> None:
        """Выводит все параметры в формате ключ-значение"""
        params = self.get_all_parameters()
        print("Настроенные параметры:")
        for key, value in params.items():
            print(f"  {key}: {value}")