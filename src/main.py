import sys
import os
from config import Config
from dependency_parser import DependencyParser

def main():
    try:
        # Этап 1: Конфигурация
        print("🚀 ЗАПУСК СИСТЕМЫ АНАЛИЗА ЗАВИСИМОСТЕЙ")
        print("=" * 50)
        
        config = Config()
        config.load_from_csv('config.csv')
        config.display_parameters()
        
        print("\n✅ ЭТАП 1: КОНФИГУРАЦИЯ ЗАВЕРШЕНА")
        
        # Этап 2: Парсинг зависимостей
        print("\n" + "=" * 50)
        print("ЭТАП 2: ПАРСИНГ ЗАВИСИМОСТЕЙ")
        print("=" * 50)
        
        parser = DependencyParser(config)
        parser.display_dependencies()
        
        print("\n✅ ЭТАП 2: ПАРСИНГ ЗАВИСИМОСТЕЙ ЗАВЕРШЕН")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()