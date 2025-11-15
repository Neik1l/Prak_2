from typing import Dict, List, Set, Optional
from config import Config
from dependency_parser import DependencyParser

class DependencyGraph:
    def __init__(self, config: Config):
        self.config = config
        self.graph: Dict[str, List[str]] = {}
        self.reverse_graph: Dict[str, List[str]] = {}
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
            # Для реальных пакетов пока используем тестовые данные для демонстрации
            print("Режим работы с GitHub будет реализован в следующих этапах")
            return
        
        # Строим обратный граф после построения основного
        self._build_reverse_graph()
        
        print(f"Граф построен. Найдено пакетов: {len(self.graph)}")
        if self.cycles:
            print(f"Обнаружено циклических зависимостей: {len(self.cycles)}")
    
    def _build_reverse_graph(self) -> None:
        """Строит обратный граф зависимостей"""
        self.reverse_graph = {}
        
        # Для каждого пакета в графе
        for package in self.graph:
            self.reverse_graph[package] = []
        
        # Заполняем обратные зависимости
        for package, dependencies in self.graph.items():
            for dep in dependencies:
                if dep in self.reverse_graph:
                    self.reverse_graph[dep].append(package)
                else:
                    self.reverse_graph[dep] = [package]
    
    def find_reverse_dependencies(self, package: str) -> List[str]:
        """Находит все обратные зависимости для заданного пакета"""
        if package not in self.reverse_graph:
            return []
        
        return sorted(self.reverse_graph[package])
    
    def find_transitive_reverse_dependencies(self, package: str) -> Set[str]:
        """Находит все транзитивные обратные зависимости (пакеты, которые прямо или косвенно зависят от данного)"""
        if package not in self.reverse_graph:
            return set()
        
        visited = set()
        result = set()
        
        def dfs_reverse(current: str):
            if current in visited:
                return
            visited.add(current)
            
            # Добавляем прямые обратные зависимости
            if current in self.reverse_graph:
                for reverse_dep in self.reverse_graph[current]:
                    result.add(reverse_dep)
                    dfs_reverse(reverse_dep)
        
        # Запускаем DFS из исходного пакета
        dfs_reverse(package)
        return result
    
    def display_reverse_dependencies(self, package: str) -> None:
        """Выводит обратные зависимости для заданного пакета"""
        print(f"\nПоиск обратных зависимостей для пакета '{package}':")
        
        direct_reverse = self.find_reverse_dependencies(package)
        transitive_reverse = self.find_transitive_reverse_dependencies(package)
        
        if not direct_reverse and not transitive_reverse:
            print("  Обратные зависимости не найдены")
            return
        
        if direct_reverse:
            print(f"  Прямые обратные зависимости ({len(direct_reverse)}):")
            for i, dep in enumerate(direct_reverse, 1):
                print(f"    {i}. {dep}")
        
        if transitive_reverse and len(transitive_reverse) > len(direct_reverse):
            transitive_only = transitive_reverse - set(direct_reverse)
            if transitive_only:
                print(f"  Транзитивные обратные зависимости ({len(transitive_only)}):")
                for i, dep in enumerate(sorted(transitive_only), 1):
                    print(f"    {i}. {dep}")
    
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
                content = f.read().strip()
            
            test_data = {}
            lines = content.split('\n')
            current_package = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    current_package = None
                    continue
                
                # Если строка состоит из одной заглавной буквы - это пакет
                if len(line) == 1 and line.isupper():
                    current_package = line
                    if current_package not in test_data:
                        test_data[current_package] = []
                # Иначе это зависимость текущего пакета
                elif current_package and len(line) == 1 and line.isupper():
                    test_data[current_package].append(line)
            
            return test_data
            
        except Exception as e:
            raise ValueError(f"Ошибка загрузки тестовых данных: {e}")
    
    def display_graph(self) -> None:
        """Выводит граф зависимостей"""
        print(f"\nПолный граф зависимостей для '{self.config.package_name}':")
        
        for package, dependencies in sorted(self.graph.items()):
            if dependencies:
                print(f"  {package} -> {', '.join(dependencies)}")
            else:
                print(f"  {package} -> (нет зависимостей)")
        
        if self.cycles:
            print(f"\nОбнаружены циклические зависимости:")
            for i, cycle in enumerate(self.cycles, 1):
                print(f"  {i}. {' -> '.join(cycle)}")