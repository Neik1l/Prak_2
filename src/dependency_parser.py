import os
import tempfile
import urllib.request
import urllib.error
import re
from typing import List, Dict, Any
from config import Config

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
            return self._parse_dependencies_simple(cargo_toml_content)
            
        except Exception as e:
            raise ValueError(f"Ошибка получения зависимостей из GitHub: {e}")
    
    def _get_cargo_toml_url(self) -> str:
        """Формирует URL для скачивания Cargo.toml"""
        repo_url = self.config.repository_url.rstrip('/')
        
        # Преобразуем GitHub URL в raw URL
        if 'github.com' in repo_url:
            parts = repo_url.replace('https://github.com/', '').split('/')
            if len(parts) >= 2:
                user, repo = parts[0], parts[1]
                branches = ['main', 'master']
                for branch in branches:
                    test_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/Cargo.toml"
                    if self._url_exists(test_url):
                        return test_url
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
    
    def _parse_dependencies_simple(self, content: str) -> List[str]:
        """Упрощенный парсер для извлечения зависимостей из Cargo.toml"""
        dependencies = []
        in_dependencies_section = False
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Начало секции зависимостей
            if line == '[dependencies]':
                in_dependencies_section = True
                continue
            # Конец секции (новая секция)
            elif line.startswith('[') and in_dependencies_section:
                break
            
            # В секции зависимостей - извлекаем имена
            if in_dependencies_section and '=' in line and not line.startswith('#'):
                dep_name = line.split('=')[0].strip()
                if dep_name and not dep_name.startswith('['):
                    dependencies.append(dep_name)
        
        return dependencies
    
    def _get_dependencies_from_test_repo(self) -> List[str]:
        """Получает зависимости из тестового репозитория"""
        # Для этапа 3 будет реализовано в dependency_graph
        return []
    
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