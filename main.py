import time
import threading
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext
from generator import UsernameGenerator
from parser import FragmentParser

class UsernameCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Username Checker")
        self.root.geometry("900x700")
        
        self.generator = UsernameGenerator()
        self.parser = FragmentParser()
        self.running = False
        self.available_usernames = []
        self.total_checked = 0
        self.total_found = 0
        self.start_time = None
        self.current_category = "4char"  # Категория по умолчанию
        
        self.setup_ui()
        
    def setup_ui(self):
        # Создаем вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка 1: Главная (кнопки и логи)
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Главная")
        
        # Вкладка 2: Доступные юзернеймы
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Доступные юзернеймы")
        
        self.setup_main_tab()
        self.setup_results_tab()
        
    def setup_main_tab(self):
        # Верхняя панель с кнопками и выбором категории
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # Выбор категории
        category_frame = ttk.LabelFrame(control_frame, text="Выбор категории")
        category_frame.pack(side='left', fill='y', padx=5)
        
        self.category_var = tk.StringVar(value="4char")
        
        ttk.Radiobutton(category_frame, text="4-символьные", variable=self.category_var, 
                       value="4char", command=self.update_category).pack(anchor='w')
        ttk.Radiobutton(category_frame, text="5-символьные", variable=self.category_var, 
                       value="5char", command=self.update_category).pack(anchor='w')
        ttk.Radiobutton(category_frame, text="Английские слова", variable=self.category_var, 
                       value="english", command=self.update_category).pack(anchor='w')
        
        # Кнопки управления
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side='right', fill='y', padx=5)
        
        self.start_button = ttk.Button(button_frame, text="▶️ Старт", command=self.start_checking)
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="⏹️ Стоп", command=self.stop_checking, state='disabled')
        self.stop_button.pack(side='left', padx=5)
        
        self.save_button = ttk.Button(button_frame, text="💾 Сохранить", command=self.save_results)
        self.save_button.pack(side='left', padx=5)
        
        self.refresh_button = ttk.Button(button_frame, text="🔄 Обновить", command=self.update_results_tab)
        self.refresh_button.pack(side='left', padx=5)
        
        # Статистика
        stats_frame = ttk.LabelFrame(self.main_frame, text="Статистика")
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="Ожидание запуска...")
        self.stats_label.pack(padx=10, pady=5)
        
        # Логи
        log_frame = ttk.LabelFrame(self.main_frame, text="Логи в реальном времени")
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=100)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        self.log_text.config(state='disabled')
        
    def setup_results_tab(self):
        # Таблица с доступными юзернеймами
        results_frame = ttk.Frame(self.results_frame)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Заголовок
        self.results_label = ttk.Label(results_frame, text="Доступные юзернеймы не найдены")
        self.results_label.pack(pady=5)
        
        # Таблица
        columns = ('username', 'status', 'response_time', 'url')
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=15)
        
        self.results_tree.heading('username', text='Юзернейм')
        self.results_tree.heading('status', text='Статус')
        self.results_tree.heading('response_time', text='Время ответа')
        self.results_tree.heading('url', text='Ссылка')
        
        self.results_tree.column('username', width=120)
        self.results_tree.column('status', width=100)
        self.results_tree.column('response_time', width=80)
        self.results_tree.column('url', width=200)
        
        # Скроллбар для таблицы
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        self.results_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def update_category(self):
        """Обновляет выбранную категорию"""
        self.current_category = self.category_var.get()
        self.log_message(f"📁 Выбрана категория: {self.get_category_name()}")
        
    def get_category_name(self):
        """Возвращает название категории"""
        categories = {
            "4char": "4-символьные",
            "5char": "5-символьные", 
            "english": "Английские слова"
        }
        return categories.get(self.current_category, "4-символьные")
        
    def log_message(self, message):
        """Добавляет сообщение в лог"""
        self.log_text.config(state='normal')
        self.log_text.insert('end', message + '\n')
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        
    def update_stats(self):
        """Обновляет статистику"""
        if self.start_time:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            speed = self.total_checked / (elapsed / 60) if elapsed > 0 else 0
            
            stats_text = (f"📊 Проверено: {self.total_checked} | "
                         f"🎯 Найдено: {self.total_found} | "
                         f"🚀 Скорость: {speed:.0f}/мин | "
                         f"⏱️ Время: {elapsed:.0f} сек | "
                         f"📁 Категория: {self.get_category_name()} | "
                         f"🎲 Уникальных: {len(self.generator.used_usernames)}")
            self.stats_label.config(text=stats_text)
        
    def update_results_tab(self):
        """Обновляет вкладку с результатами"""
        # Очищаем таблицу
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        if self.available_usernames:
            self.results_label.config(text=f"Найдено {len(self.available_usernames)} доступных юзернеймов")
            
            for user in self.available_usernames:
                self.results_tree.insert('', 'end', values=(
                    user['username'],
                    user['status'],
                    f"{user['response_time']}с",
                    user['url']
                ))
        else:
            self.results_label.config(text="Доступные юзернеймы не найдены")
            
    def save_results(self):
        """Сохраняет результаты в файл"""
        if not self.available_usernames:
            self.log_message("❌ Нет доступных юзернеймов для сохранения")
            return
            
        filename = f"available_usernames_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("🎯 ДОСТУПНЫЕ ЮЗЕРНЕЙМЫ НА FRAGMENT.COM\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Категория: {self.get_category_name()}\n")
                f.write(f"Всего проверено: {self.total_checked} юзернеймов\n")
                f.write(f"Найдено доступных: {len(self.available_usernames)}\n")
                f.write(f"Время начала: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Время сохранения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                for user in self.available_usernames:
                    f.write(f"🔹 Юзернейм: {user['username']}\n")
                    f.write(f"🔗 Ссылка:   {user['url']}\n")
                    f.write(f"📊 Статус:   {user['status']}\n")
                    f.write(f"⏱️  Время ответа: {user.get('response_time', 0)}с\n")
                    f.write("-" * 40 + "\n")
            
            self.log_message(f"💾 Сохранено в {filename}")
            
        except Exception as e:
            self.log_message(f"❌ Ошибка при сохранении: {e}")
            
    def start_checking(self):
        """Запускает проверку в отдельном потоке"""
        if not self.running:
            self.running = True
            self.start_time = datetime.now()
            self.available_usernames = []
            self.total_checked = 0
            self.total_found = 0
            
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            
            self.log_message("🚀 Запуск проверки...")
            self.log_message(f"📁 Категория: {self.get_category_name()}")
            self.log_message("⏹️ Для остановки нажмите кнопку 'Стоп'")
            self.log_message("=" * 50)
            
            # Запускаем в отдельном потоке
            self.check_thread = threading.Thread(target=self.run_continuous, daemon=True)
            self.check_thread.start()
            
    def stop_checking(self):
        """Останавливает проверку"""
        if self.running:
            self.running = False
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            
            self.log_message("🛑 Проверка остановлена")
            self.log_message(f"🎯 Итого: {self.total_checked} проверено, {self.total_found} найдено")
            
            # Обновляем таблицу результатов после остановки
            self.update_results_tab()
            
    def check_batch(self):
        """Проверка одного батча юзернеймов"""
        usernames = self.generator.generate_batch(40, self.current_category)
        self.log_message(f"🎲 Сгенерировано: {len(usernames)} юзернеймов")
        if usernames:
            self.log_message(f"📋 Примеры: {', '.join(usernames[:3])}...")
        
        results = self.parser.check_usernames_batch(usernames)
        
        # Обновляем статистику
        self.total_checked += len(usernames)
        
        # Анализируем результаты
        successful = sum(1 for r in results if r['success'])
        available = [r for r in results if r['available']]
        errors = len(results) - successful
        
        # Логируем результаты батча
        self.log_message(f"📊 Результаты батча:")
        self.log_message(f"   ✅ Успешных: {successful}/{len(usernames)}")
        self.log_message(f"   ❌ Ошибок: {errors}")
        self.log_message(f"   🎯 Доступных: {len(available)}")
        
        if available:
            self.available_usernames.extend(available)
            self.total_found += len(available)
            self.log_message(f"   🎉 НАЙДЕНО ДОСТУПНЫХ:")
            for user in available:
                self.log_message(f"      🔹 {user['username']} - {user['status']} ({user['response_time']}s)")
            
            # Обновляем таблицу результатов
            self.update_results_tab()
        
        return len(available)
    
    def run_continuous(self):
        """Бесконечный цикл проверки (запускается в потоке)"""
        batch_count = 0
        
        try:
            while self.running:
                batch_count += 1
                self.log_message(f"\n📦 БАТЧ #{batch_count}")
                self.log_message("=" * 40)
                
                found = self.check_batch()
                
                # Обновляем статистику в UI
                self.root.after(0, self.update_stats)
                
                # Очищаем историю каждые 10 батчей чтобы не засорять память
                if batch_count % 10 == 0:
                    self.generator.clear_used_usernames()
                    self.log_message("🧹 История юзернеймов очищена")
                
                # Короткая пауза между батчами
                time.sleep(2)
                
        except Exception as e:
            self.log_message(f"❌ Ошибка: {e}")
        finally:
            self.root.after(0, self.stop_checking)

def main():
    """Запуск приложения"""
    root = tk.Tk()
    app = UsernameCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()