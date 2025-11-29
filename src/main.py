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
        print("\n🎉 Все этапы завершены успешно!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()