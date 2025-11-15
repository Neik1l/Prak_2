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
        else:
            # Режим тестирования - только граф
            print("\n🔧 Режим тестирования")
            graph = DependencyGraph(config)
            graph.build_graph()
            graph.display_graph()
        
        print("\nЭтап 3 завершен успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()