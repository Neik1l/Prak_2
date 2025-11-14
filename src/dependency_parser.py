import os
import tempfile
import urllib.request
import urllib.error
import toml
from typing import List, Dict, Any
from toml import loads as toml_loads

class DependencyParser:
    def __init__(self, config):
        self.config = config
        self.dependencies = []
    
    def get_dependencies(self) -> List[str]:
        """Получает прямые зависимости пакета"""
        if self.config.test_mode:
            return self._get_dependencies_from_test_repo()
        else:
            return self._get_dependencies_from_github()
    
    def _get_dependencies_from_github(self) -> List[str]:
        """Получает зависимости из GitHub репозитория"""
        try:
            # Формируем URL к raw Cargo.toml файлу
            cargo_toml_url = self._get_cargo_toml_url()
            print(f"Загрузка Cargo.toml из: {cargo_toml_url}")
            
            # Скачиваем Cargo.toml
            cargo_toml_content = self._download_file(cargo_toml_url)
            
            # Парсим зависимости
            return self._parse_dependencies_from_content(cargo_toml_content)
            
        except Exception as e:
            raise ValueError(f"Ошибка получения зависимостей из GitHub: {e}")
    
    def _get_cargo_toml_url(self) -> str:
        """Формирует URL для скачивания Cargo.toml"""
        repo_url = self.config.repository_url.rstrip('/')
        
        # Преобразуем GitHub URL в raw URL
        if 'github.com' in repo_url:
            # Пример: https://github.com/rust-lang/log -> https://raw.githubusercontent.com/rust-lang/log/main/Cargo.toml
            parts = repo_url.replace('https://github.com/', '').split('/')
            if len(parts) >= 2:
                user, repo = parts[0], parts[1]
                # Пробуем разные ветки
                branches = ['main', 'master', 'trunk']
                for branch in branches:
                    test_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/Cargo.toml"
                    if self._url_exists(test_url):
                        return test_url
                
                # Если ни одна ветка не найдена, используем main
                return f"https://raw.githubusercontent.com/{user}/{repo}/main/Cargo.toml"
        
        raise ValueError(f"Неподдерживаемый URL репозитория: {repo_url}")
    
    def _url_exists(self, url: str) -> bool:
        """Проверяет существует ли URL"""
        try:
            with urllib.request.urlopen(url) as response:
                return response.getcode() == 200
        except:
            return False
    
    def _download_file(self, url: str) -> str:
        """Скачивает файл по URL и возвращает его содержимое"""
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                return content
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValueError(f"Файл Cargo.toml не найден по URL: {url}")
            else:
                raise ValueError(f"Ошибка HTTP {e.code} при загрузке файла")
        except urllib.error.URLError as e:
            raise ValueError(f"Ошибка сети: {e.reason}")
    
    def _parse_dependencies_from_content(self, content: str) -> List[str]:
        """Парсит зависимости из содержимого Cargo.toml"""
        try:
            # Парсим TOML
            cargo_data = toml.loads(content)
            
            dependencies = []
            
            # Извлекаем зависимости из разных секций
            dependency_sections = ['dependencies', 'dev-dependencies', 'build-dependencies']
            
            for section in dependency_sections:
                if section in cargo_data:
                    deps = cargo_data[section]
                    
                    for dep_name, dep_info in deps.items():
                        if isinstance(dep_info, str):
                            # Простая зависимость: name = "version"
                            dependencies.append(dep_name)
                        elif isinstance(dep_info, dict):
                            # Сложная зависимость: name = { ... }
                            dependencies.append(dep_name)
                        else:
                            dependencies.append(dep_name)
            
            # Убираем дубликаты и сортируем
            return sorted(list(set(dependencies)))
            
        except toml.TomlDecodeError as e:
            raise ValueError(f"Ошибка парсинга TOML: {e}")
        except Exception as e:
            raise ValueError(f"Ошибка обработки Cargo.toml: {e}")
    
    def _get_dependencies_from_test_repo(self) -> List[str]:
        """Получает зависимости из тестового репозитория (для этапа 3)"""
        # Пока заглушка - реализуем в этапе 3
        raise ValueError("Тестовый режим будет реализован в этапе 3")
    
    def display_dependencies(self) -> None:
        """Выводит прямые зависимости на экран"""
        try:
            dependencies = self.get_dependencies()
            print(f"\nПрямые зависимости пакета '{self.config.package_name}':")
            
            if not dependencies:
                print("  Зависимости не найдены")
            else:
                for i, dep in enumerate(dependencies, 1):
                    print(f"  {i}. {dep}")
                    
        except Exception as e:
            print(f"Ошибка при получении зависимостей: {e}")