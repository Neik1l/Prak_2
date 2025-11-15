from typing import Dict, List
from dependency_graph import DependencyGraph

class GraphVisualizer:
    def __init__(self, graph: DependencyGraph):
        self.graph = graph
    
    def generate_mermaid_graph(self) -> str:
        """Генерирует Mermaid диаграмму графа зависимостей"""
        mermaid_lines = ["graph TD"]
        
        # Добавляем все узлы и связи
        for package, dependencies in sorted(self.graph.graph.items()):
            if dependencies:
                for dep in dependencies:
                    # Для циклических зависимостей добавляем специальный стиль
                    is_cyclic = self._is_cyclic_connection(package, dep)
                    if is_cyclic:
                        mermaid_lines.append(f"    {package} -.-> {dep}")
                    else:
                        mermaid_lines.append(f"    {package} --> {dep}")
            else:
                # Пакет без зависимостей
                mermaid_lines.append(f"    {package}")
        
        # Добавляем стили для циклических зависимостей
        if self.graph.cycles:
            mermaid_lines.append("    linkStyle default stroke:red,stroke-width:1px")
        
        return "\n".join(mermaid_lines)
    
    def _is_cyclic_connection(self, package: str, dep: str) -> bool:
        """Проверяет является ли связь частью цикла"""
        for cycle in self.graph.cycles:
            for i in range(len(cycle) - 1):
                if cycle[i] == package and cycle[i + 1] == dep:
                    return True
            # Проверяем замыкание цикла
            if len(cycle) > 1 and cycle[0] == dep and cycle[-1] == package:
                return True
        return False
    
    def generate_mermaid_reverse_graph(self, target_package: str) -> str:
        """Генерирует Mermaid диаграмму обратных зависимостей"""
        mermaid_lines = ["graph TD"]
        
        # Находим все обратные зависимости
        reverse_deps = list(self.graph.find_transitive_reverse_dependencies(target_package))
        
        if not reverse_deps:
            mermaid_lines.append(f"    {target_package}")
            return "\n".join(mermaid_lines)
        
        # Добавляем связи от зависимых пакетов к целевому
        for dep_package in sorted(reverse_deps):
            mermaid_lines.append(f"    {dep_package} --> {target_package}")
        
        # Выделяем целевой пакет
        mermaid_lines.append(f"    style {target_package} fill:#f9f,stroke:#333,stroke-width:2px")
        
        return "\n".join(mermaid_lines)
    
    def display_mermaid_graph(self) -> None:
        """Выводит Mermaid диаграмму на экран"""
        mermaid_code = self.generate_mermaid_graph()
        
        print("\n" + "🔮" * 20)
        print("Mermaid диаграмма графа зависимостей:")
        print("🔮" * 20)
        print("\n```mermaid")
        print(mermaid_code)
        print("```")
        
        print("\n💡 Скопируйте код выше в Mermaid Live Editor:")
        print("   https://mermaid.live/")
        print("   или в Markdown файл с поддержкой Mermaid")
    
    def display_reverse_mermaid_graph(self, target_package: str) -> None:
        """Выводит Mermaid диаграмму обратных зависимостей"""
        mermaid_code = self.generate_mermaid_reverse_graph(target_package)
        
        print(f"\n Mermaid диаграмма обратных зависимостей для '{target_package}':")
        print("\n```mermaid")
        print(mermaid_code)
        print("```")
    
    def save_mermaid_to_file(self, filename: str = "dependency_graph.mmd") -> None:
        """Сохраняет Mermaid код в файл"""
        mermaid_code = self.generate_mermaid_graph()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(mermaid_code)
        
        print(f"\n Mermaid код сохранен в файл: {filename}")
    
    def compare_with_std_tools(self) -> None:
        """Сравнивает результаты с штатными инструментами"""
        print("\n" + "📊" * 20)
        print("Сравнение с штатными инструментами:")
        print("📊" * 20)
        
        print("\n1.  Граф зависимостей нашего инструмента:")
        all_packages = set(self.graph.graph.keys())
        all_dependencies = set()
        for deps in self.graph.graph.values():
            all_dependencies.update(deps)
        
        print(f"   - Всего пакетов: {len(all_packages)}")
        print(f"   - Всего зависимостей: {sum(len(deps) for deps in self.graph.graph.values())}")
        print(f"   - Циклические зависимости: {len(self.graph.cycles)}")
        
        print("\n2.  Особенности нашего решения:")
        print("   - Обнаружение циклических зависимостей ✅")
        print("   - Обратные зависимости ✅") 
        print("   - Визуализация Mermaid ✅")
        print("   - Тестовый режим ✅")
        
        print("\3.   Возможные расхождения:")
        print("   - Мы используем упрощенный парсер Cargo.toml")
        print("   - Не обрабатываем условные зависимости (features)")
        print("   - Не учитываем версии пакетов")
        print("   - Для зависимостей используем тот же репозиторий")