from config import Config
from dependency_parser import DependencyParser
from dependency_graph import DependencyGraph
from visualizer import GraphVisualizer
from png_visualizer import PNGVisualizer  # Добавляем новый импорт
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
            # Режим тестирования - полная демонстрация
            print("\n🔧 Режим тестирования")
            graph = DependencyGraph(config)
            graph.build_graph()
            graph.display_graph()
            
            # Этап 4: Демонстрация обратных зависимостей
            print("\n" + "="*50)
            print("ЭТАП 4: ОБРАТНЫЕ ЗАВИСИМОСТИ")
            print("="*50)
            
            test_packages = ['A', 'C', 'E', 'F']
            for package in test_packages:
                graph.display_reverse_dependencies(package)
                print()
        
        # Этап 5: Визуализация
        print("\n" + "="*50)
        print("ЭТАП 5: ВИЗУАЛИЗАЦИЯ")
        print("="*50)
        
        # 5.1 Mermaid диаграмма (ваш существующий код)
        visualizer = GraphVisualizer(graph)
        visualizer.display_mermaid_graph()
        
        # 5.2 PNG визуализация (НОВОЕ!)
        png_visualizer = PNGVisualizer(graph)
        png_visualizer.display_all_visualizations()
        
        # 5.3 Mermaid диаграммы обратных зависимостей для 3 пакетов
        print("\n" + "-"*30)
        print("Mermaid визуализация обратных зависимостей:")
        print("-"*30)
        
        demo_packages = ['C', 'E', 'F'] if config.test_mode else [config.package_name]
        for package in demo_packages:
            visualizer.display_reverse_mermaid_graph(package)
            print()
        
        # 5.4 Сохранение в файл
        visualizer.save_mermaid_to_file()
        
        # 5.5 Сравнение с штатными инструментами
        visualizer.compare_with_std_tools()
        
        print("\n🎉 Все этапы завершены успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()