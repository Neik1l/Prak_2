from config import Config
from dependency_parser import DependencyParser
from dependency_graph import DependencyGraph
import sys
import os

def main():
    try:
        # Загружаем конфигурацию
        config = Config()
        config.load_from_csv('config.csv')
        
        # Выводим параметры (требование этапа 1)
        config.display_parameters()
        
        if not config.test_mode:
            # Этап 2: Прямые зависимости
            parser = DependencyParser(config)
            parser.display_dependencies()
            
            # Этап 3: Полный граф зависимостей
            graph = DependencyGraph(config)
            graph.build_graph()
            graph.display_graph()
            
            # Этап 4: Обратные зависимости для основного пакета
            graph.display_reverse_dependencies(config.package_name)
            
        else:
            # Режим тестирования - граф и обратные зависимости
            print("\n🔧 Режим тестирования")
            graph = DependencyGraph(config)
            graph.build_graph()
            graph.display_graph()
            
            # Этап 4: Демонстрация обратных зависимостей для разных пакетов
            print("\n" + "="*50)
            print("ЭТАП 4: ДОПОЛНИТЕЛЬНЫЕ ОПЕРАЦИИ")
            print("="*50)
            
            # Тестируем обратные зависимости для разных пакетов
            test_packages = ['A', 'C', 'E', 'F']
            for package in test_packages:
                graph.display_reverse_dependencies(package)
                print()
        
        print("\nЭтап 4 завершен успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()