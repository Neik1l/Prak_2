from typing import Dict, List, Set
from config import Config
from dependency_parser import DependencyParser

class DependencyGraph:
    def __init__(self, config: Config):
        self.config = config
        self.graph: Dict[str, List[str]] = {}
        self.visited: Set[str] = set()
        self.recursion_stack: Set[str] = set()
        self.cycles: List[List[str]] = []
    
    def build_graph(self) -> None:
        """Строит полный граф зависимостей с помощью DFS"""
        start_package = self.config.package_name
        print(f"Построение графа зависимостей для пакета: {start_package}")
        
        if self.config.test_mode:
            self._build_from_test_repo(start_package)
        else:
            self._build_from_github(start_package)
        
        print(f"Граф построен. Найдено пакетов: {len(self.graph)}")
        if self.cycles:
            print(f"Обнаружено циклических зависимостей: {len(self.cycles)}")
    
    def _build_from_github(self, package: str) -> None:
        """Рекурсивно строит граф из GitHub репозиториев"""
        if package in self.visited:
            return
        
        # Проверка на цикличность
        if package in self.recursion_stack:
            cycle = list(self.recursion_stack) + [package]
            self.cycles.append(cycle)
            print(f"Обнаружена циклическая зависимость: {' -> '.join(cycle)}")
            return
        
        self.recursion_stack.add(package)
        self.visited.add(package)
        
        try:
            # Получаем зависимости для текущего пакета
            dependencies = self._get_dependencies_for_package(package)
            self.graph[package] = dependencies
            
            print(f"{package} -> {dependencies}")
            
            # Рекурсивно обрабатываем зависимости
            for dep in dependencies:
                self._build_from_github(dep)
                
        except Exception as e:
            print(f"Ошибка при обработке пакета {package}: {e}")
            self.graph[package] = []
        finally:
            self.recursion_stack.remove(package)
    
    def _get_dependencies_for_package(self, package: str) -> List[str]:
        """Получает зависимости для конкретного пакета"""
        if self.config.test_mode:
            return self._get_test_dependencies(package)
        else:
            # Для реальных пакетов используем тот же репозиторий что и основной пакет
            # В реальной реализации здесь был бы поиск репозитория для каждого пакета
            if package == self.config.package_name:
                parser = DependencyParser(self.config)
                return parser.get_dependencies()
            else:
                # Заглушка - в реальности нужно искать репозитории зависимостей
                return []
    
    def _build_from_test_repo(self, package: str) -> None:
        """Строит граф из тестового репозитория"""
        test_data = self._load_test_data()
        
        if package not in test_data:
            print(f"Пакет {package} не найден в тестовых данных")
            return
        
        self._dfs_test(package, test_data)
    
    def _dfs_test(self, package: str, test_data: Dict[str, List[str]]) -> None:
        """DFS для тестовых данных"""
        if package in self.visited:
            return
        
        if package in self.recursion_stack:
            cycle = list(self.recursion_stack) + [package]
            self.cycles.append(cycle)
            print(f"Обнаружена циклическая зависимость: {' -> '.join(cycle)}")
            return
        
        self.recursion_stack.add(package)
        self.visited.add(package)
        
        dependencies = test_data.get(package, [])
        self.graph[package] = dependencies
        
        print(f"{package} -> {dependencies}")
        
        for dep in dependencies:
            self._dfs_test(dep, test_data)
        
        self.recursion_stack.remove(package)
    
    def _load_test_data(self) -> Dict[str, List[str]]:
        """Загружает тестовые данные из файла"""
        try:
            with open(self.config.test_repo_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            test_data = {}
            current_package = None
            
            for line in content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.isupper() and len(line) == 1:  # Однобуквенные имена пакетов
                    current_package = line
                    test_data[current_package] = []
                elif current_package and line.isupper() and len(line) == 1:
                    test_data[current_package].append(line)
            
            return test_data
            
        except Exception as e:
            raise ValueError(f"Ошибка загрузки тестовых данных: {e}")
    
    def _get_test_dependencies(self, package: str) -> List[str]:
        """Получает зависимости из тестовых данных"""
        test_data = self._load_test_data()
        return test_data.get(package, [])
    
    def display_graph(self) -> None:
        """Выводит граф зависимостей"""
        print(f"\nПолный граф зависимостей для '{self.config.package_name}':")
        
        for package, dependencies in self.graph.items():
            if dependencies:
                print(f"  {package} -> {', '.join(dependencies)}")
            else:
                print(f"  {package} -> (нет зависимостей)")
        
        if self.cycles:
            print(f"\nОбнаружены циклические зависимости:")
            for i, cycle in enumerate(self.cycles, 1):
                print(f"  {i}. {' -> '.join(cycle)}")
    
    def get_all_dependencies(self) -> Set[str]:
        """Возвращает все уникальные зависимости (транзитивные)"""
        all_deps = set()
        for deps in self.graph.values():
            all_deps.update(deps)
        return all_deps