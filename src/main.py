import sys
import os
from config import Config  # Теперь импорт проще

def main():
    try:
        # Загружаем конфигурацию
        config = Config()
        config.load_from_csv('config.csv')
        
        # Выводим параметры (требование этапа 1)
        config.display_parameters()
        
        print("\nКонфигурация успешно загружена!")
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()