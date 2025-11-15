import csv

class Config:
    def __init__(self):
        self.package_name = ""
        self.test_mode = False
        self.test_repo_path = ""
        self.max_depth = 3
        self.repository_url = ""
    
    def load_from_csv(self, filename: str):
        """Загружает конфигурацию из CSV файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.package_name = row.get('package_name', '').strip()
                    
                    # Обрабатываем test_mode
                    test_mode_str = row.get('test_mode', '').strip().lower()
                    self.test_mode = test_mode_str in ['true', '1', 'yes', 'да']
                    
                    self.test_repo_path = row.get('test_repo_path', '').strip()
                    self.repository_url = row.get('repository_url', '').strip()
                    
                    # Обрабатываем max_depth
                    max_depth_str = row.get('max_depth', '').strip()
                    if max_depth_str:
                        self.max_depth = int(max_depth_str)
                    else:
                        self.max_depth = 3
                    
            print("✅ Конфигурация загружена из config.csv")
            
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            raise
    
    def display_parameters(self):
        """Выводит параметры конфигурации"""
        print("\n⚙️ КОНФИГУРАЦИЯ СИСТЕМЫ")
        print("-" * 30)
        print(f"📦 Основной пакет: {self.package_name}")
        print(f"🔧 Режим тестирования: {'Да' if self.test_mode else 'Нет'}")
        print(f"📊 Макс. глубина анализа: {self.max_depth}")
        print(f"🌐 URL репозитория: {self.repository_url}")
        if self.test_repo_path:
            print(f"📁 Тестовый путь: {self.test_repo_path}")