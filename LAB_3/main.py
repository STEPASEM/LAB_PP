import tkinter as tk
import pyperclip
import time

from deep_translator import GoogleTranslator
from tkinter import ttk, messagebox

from languages_ru import RUSSIAN_LANG_NAMES

class Translators:
    def __init__(self, root):
        self.root = root
        self.root.title("ПЕРЕВОДЧИК")
        self.root.geometry("600x500")  # Увеличил высоту немного
        self.root.configure(bg="#f0f0f0")

        self.russian_lang_names = RUSSIAN_LANG_NAMES
        self.auto_translate_timer = None
        self.last_key_time = 0
        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="ПЕРЕВОДЧИК",
            font=("Arial", 24, "bold"),
            bg="#f0f0f0",
            fg="#2c3e50"
        )
        title_label.pack(pady=15)

        # Фрейм для выбора языков
        lang_frame = tk.Frame(self.root, bg="#f0f0f0")
        lang_frame.pack(pady=10)

        # Список языков на русском (отсортированный)
        russian_lang_list = sorted(self.russian_lang_names.values())

        self.src_lang = ttk.Combobox(
            lang_frame,
            values=russian_lang_list,
            width=25,
            font=("Arial", 10),
            state="readonly"
        )
        self.src_lang.grid(row=0, column=1, padx=5)
        self.src_lang.set('русский')

        # Кнопка-стрелка для обмена языками
        swap_btn = tk.Button(
            lang_frame,
            text="⇄",
            font=("Arial", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=3,
            command=self.swap_languages,
            relief="flat",
            cursor="hand2"
        )
        swap_btn.grid(row=0, column=2, padx=10)

        self.dest_lang = ttk.Combobox(
            lang_frame,
            values=russian_lang_list,
            width=25,
            font=("Arial", 10),
            state="readonly"
        )
        self.dest_lang.grid(row=0, column=4, padx=5)
        self.dest_lang.set('английский')
        # Связываем изменение языка
        self.dest_lang.bind('<<ComboboxSelected>>', self.translate_text)

        # Фрейм для текстовых полей
        text_frame = tk.Frame(self.root, bg="#f0f0f0")
        text_frame.pack(pady=15, padx=20, fill="both", expand=True)

        # Левое поле - ввод текста
        input_container = tk.Frame(text_frame, bg="white", relief="solid", borderwidth=1)
        input_container.grid(row=0, column=0, padx=(0, 10), sticky="nsew", ipady=5)
        text_frame.grid_columnconfigure(0, weight=1)

        tk.Label(
            input_container,
            text="Введите текст:",
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(5, 0))

        # Поле ввода с полосой прокрутки
        input_text_frame = tk.Frame(input_container, bg="white")
        input_text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.input_text = tk.Text(
            input_text_frame,
            height=12,
            font=("Arial", 11),
            wrap="word",
            relief="flat",
            padx=5,
            pady=5
        )
        self.input_text.pack(side="left", fill="both", expand=True)

        input_scrollbar = ttk.Scrollbar(input_text_frame, command=self.input_text.yview)
        input_scrollbar.pack(side="right", fill="y")
        self.input_text.config(yscrollcommand=input_scrollbar.set)

        # Привязываем обработчики клавиш
        self.input_text.bind('<KeyPress>', self.on_key_press)
        self.input_text.bind('<KeyRelease>', self.on_key_release)

        input_copy_frame = tk.Frame(input_container, bg="white")
        input_copy_frame.pack(fill="x", padx=10, pady=(0, 5))

        input_copy_btn = tk.Button(
            input_copy_frame,
            text="📋",
            font=("Arial", 9),
            bg="#27ae60",
            fg="white",
            command=self.copy_input_text,
            relief="flat",
            cursor="hand2"
        )
        input_copy_btn.pack(side="right")

        # Правое поле - вывод перевода
        output_container = tk.Frame(text_frame, bg="white", relief="solid", borderwidth=1)
        output_container.grid(row=0, column=1, padx=(10, 0), sticky="nsew", ipady=5)
        text_frame.grid_columnconfigure(1, weight=1)

        tk.Label(
            output_container,
            text="Перевод:",
            font=("Arial", 11, "bold"),
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(5, 0))

        output_text_frame = tk.Frame(output_container, bg="white")
        output_text_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.output_text = tk.Text(
            output_text_frame,
            height=12,
            font=("Arial", 11),
            wrap="word",
            relief="flat",
            padx=5,
            pady=5,
            state="disabled"
        )
        self.output_text.pack(side="left", fill="both", expand=True)

        output_scrollbar = ttk.Scrollbar(output_text_frame, command=self.output_text.yview)
        output_scrollbar.pack(side="right", fill="y")
        self.output_text.config(yscrollcommand=output_scrollbar.set)

        output_copy_frame = tk.Frame(output_container, bg="white")
        output_copy_frame.pack(fill="x", padx=10, pady=(0, 5))

        output_copy_btn = tk.Button(
            output_copy_frame,
            text="📋",
            font=("Arial", 9),
            bg="#e74c3c",
            fg="white",
            command=self.copy_output_text,
            relief="flat",
            cursor="hand2"
        )
        output_copy_btn.pack(side="right")

        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        clear_btn = tk.Button(
            button_frame,
            text="ОЧИСТИТЬ",
            font=("Arial", 12, "bold"),
            bg="#7f8c8d",
            fg="white",
            width=15,
            height=2,
            command=self.clear_all,
            relief="flat",
            cursor="hand2"
        )
        clear_btn.pack(side="left", padx=10)

    def get_lang_code(self, russian_name):
        """Получаем код языка по русскому названию"""
        for code, name in self.russian_lang_names.items():
            if name == russian_name:
                return code
        return 'ru'

    def translate_text(self, *args):
        text = self.input_text.get("1.0", tk.END).strip()
        if not text or text.isspace():
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.config(state="disabled")
            return

        try:
            # Получаем коды языков
            src_code = self.get_lang_code(self.src_lang.get())
            dest_code = self.get_lang_code(self.dest_lang.get())

            # Используем GoogleTranslator
            translated_text = GoogleTranslator(
                source=src_code,
                target=dest_code
            ).translate(text)

            # Показываем результат
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", translated_text)
            self.output_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить перевод: {str(e)}")

    def on_key_press(self, event):
        """Обработка нажатия клавиши"""
        # Обновляем время последнего нажатия
        self.last_key_time = time.time()

        # Отменяем таймер паузы
        if self.auto_translate_timer:
            self.root.after_cancel(self.auto_translate_timer)
            self.auto_translate_timer = None

    def on_key_release(self, event):
        """Обработка отпускания клавиши"""
        # Если нажат пробел - переводим сразу
        if event.keysym == 'space' or event.char == ' ':
            # Ждем 50ms чтобы пробел успел добавиться
            self.root.after(50, self.delayed_translate_on_space)
            return

        # Для других клавиш - запускаем таймер на 1 секунду
        if self.auto_translate_timer:
            self.root.after_cancel(self.auto_translate_timer)

        # Запускаем таймер на проверку паузы
        self.auto_translate_timer = self.root.after(1000, self.check_pause_and_translate)

    def delayed_translate_on_space(self):
        """Отложенный перевод после пробела"""
        text = self.input_text.get("1.0", tk.END).strip()
        if text and len(text) >= 3:  # Хотя бы 3 символа
            self.translate_text()

    def check_pause_and_translate(self):
        """Проверить паузу и перевести если нужно"""
        current_time = time.time()
        time_since_last_key = current_time - self.last_key_time

        # Если прошло больше 1 секунд с последнего нажатия
        if time_since_last_key >= 1.0:
            text = self.input_text.get("1.0", tk.END).strip()
            if text and text[-1] != ' ':
                self.translate_text()

        # Сбрасываем таймер
        self.auto_translate_timer = None

    def clear_all(self):
        """Очистить все поля"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")

    def copy_input_text(self):
        """Копировать текст из поля ввода"""
        text = self.input_text.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            self.show_copy_message("Текст скопирован в буфер обмена")

    def copy_output_text(self):
        """Копировать текст из поля перевода"""
        text = self.output_text.get("1.0", tk.END).strip()
        if text:
            pyperclip.copy(text)
            self.show_copy_message("Перевод скопирован в буфер обмена")

    def show_copy_message(self, message):
        """Показать всплывающее сообщение о копировании"""
        # Создаем временную метку
        message_label = tk.Label(
            self.root,
            text=message,
            font=("Arial", 9),
            bg="#2ecc71",
            fg="white",
            padx=10,
            pady=5
        )
        message_label.place(relx=0.5, rely=0.8, anchor="center")

        # Удаляем метку через 2 секунды
        self.root.after(2000, message_label.destroy)

    def swap_languages(self):
        """Поменять языки местами"""
        current_src = self.src_lang.get()
        current_dest = self.dest_lang.get()
        self.src_lang.set(current_dest)
        self.dest_lang.set(current_src)

        # Получаем текущий перевод
        output_text = self.output_text.get("1.0", tk.END).strip()

        # Если есть перевод, перемещаем его в поле ввода
        if output_text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", output_text)

        # Очищаем поле перевода
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")

        # Проверяем, есть ли теперь текст для перевода
        current_text = self.input_text.get("1.0", tk.END).strip()
        if current_text:
            # Небольшая задержка для стабильности
            self.root.after(50, self.translate_text)


if __name__ == "__main__":
    root = tk.Tk()
    app = Translators(root)

    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()+180
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()