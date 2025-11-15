import requests
from config import Config

class DependencyParser:
    def __init__(self, config: Config):
        self.config = config
        self.dependency_cache = {}
    
    def get_dependencies(self, package_name: str):
        """Получает зависимости для пакета"""
        if package_name in self.dependency_cache:
            return self.dependency_cache[package_name]
            
        if self.config.test_mode:
            deps = self._get_test_dependencies(package_name)
        else:
            deps = self._get_real_dependencies(package_name)
            
        self.dependency_cache[package_name] = deps
        return deps
    
    def _get_test_dependencies(self, package_name: str):
        """Тестовые данные для демонстрации"""
        test_data = {
            'A': ['B', 'C'],
            'B': ['D'], 
            'C': ['E', 'F'],
            'D': [],
            'E': ['C'],  # Циклическая зависимость
            'F': ['G'],
            'G': []
        }
        return test_data.get(package_name, [])
    
    def _get_real_dependencies(self, package_name: str):
        """Получает реальные зависимости из crates.io"""
        try:
            print(f"🔍 Получение зависимостей для {package_name}...")
            url = f"https://crates.io/api/v1/crates/{package_name}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                dependencies = []
                
                # Получаем последнюю версию
                versions = data.get('versions', [])
                if versions:
                    latest = versions[0]
                    deps = latest.get('dependencies', [])
                    
                    for dep in deps:
                        if dep.get('kind') in [None, 'normal']:
                            dep_name = dep.get('crate_id')
                            if dep_name and dep_name not in dependencies:
                                dependencies.append(dep_name)
                
                print(f"📦 Пакет {package_name} имеет {len(dependencies)} зависимостей")
                return dependencies
            else:
                print(f"⚠️ Не удалось получить зависимости для {package_name} (код: {response.status_code})")
                return []
                
        except Exception as e:
            print(f"❌ Ошибка при запросе для {package_name}: {e}")
            return []
    
    def display_dependencies(self):
        """Выводит дерево зависимостей"""
        if self.config.test_mode:
            start_packages = ['A']
        else:
            start_packages = [self.config.package_name]
        
        for package in start_packages:
            print(f"\n🌳 ДЕРЕВО ЗАВИСИМОСТЕЙ ДЛЯ '{package}':")
            print("-" * 40)
            self._print_dependency_tree(package)
        
        # Проверка циклических зависимостей
        self._check_cyclic_dependencies()
    
    def _print_dependency_tree(self, package: str, depth: int = 0, path: list = None):
        """Рекурсивно печатает дерево зависимостей"""
        if path is None:
            path = []
        
        # Проверка на цикл
        if package in path:
            indent = "  " * depth
            print(f"{indent}↻ {package} (ЦИКЛ!)")
            return
        
        if depth >= self.config.max_depth:
            indent = "  " * depth
            print(f"{indent}... (достигнута максимальная глубина {self.config.max_depth})")
            return
        
        path.append(package)
        dependencies = self.get_dependencies(package)
        
        indent = "  " * depth
        if dependencies:
            deps_str = ", ".join(dependencies)
            print(f"{indent}📦 {package} → {deps_str}")
        else:
            print(f"{indent}📦 {package} → нет зависимостей")
        
        # Рекурсивно обрабатываем зависимости
        for dep in dependencies:
            self._print_dependency_tree(dep, depth + 1, path.copy())
    
    def _check_cyclic_dependencies(self):
        """Проверяет циклические зависимости"""
        print(f"\n🔍 ПРОВЕРКА ЦИКЛИЧЕСКИХ ЗАВИСИМОСТЕЙ:")
        print("-" * 40)
        
        def find_cycle(current, visited, stack):
            visited.add(current)
            stack.add(current)
            
            for dep in self.get_dependencies(current):
                if dep not in visited:
                    if find_cycle(dep, visited, stack.copy()):
                        return True
                elif dep in stack:
                    cycle_path = list(stack) + [dep]
                    print(f"⚠️ Обнаружен цикл: {' → '.join(cycle_path)}")
                    return True
            
            stack.remove(current)
            return False
        
        if self.config.test_mode:
            packages = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        else:
            packages = [self.config.package_name]
        
        cycles_found = 0
        visited = set()
        
        for package in packages:
            if package not in visited:
                if find_cycle(package, visited, set()):
                    cycles_found += 1
        
        if cycles_found == 0:
            print("✅ Циклические зависимости не обнаружены")
        else:
            print(f"📊 Найдено циклических зависимостей: {cycles_found}")