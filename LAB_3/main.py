import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator, LANGUAGES

from languages_ru import RUSSIAN_LANG_NAMES

class Translators:
    def __init__(self, root):
        self.root = root
        self.root.title("ПЕРЕВОДЧИК")
        self.root.geometry("600x400")

        self.translator = Translator()
        self.russian_lang_names = RUSSIAN_LANG_NAMES
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

        translate_btn = tk.Button(
            button_frame,
            text="ПЕРЕВЕСТИ",
            font=("Arial", 12, "bold"),
            bg="#2980b9",
            fg="white",
            width=15,
            height=2,
            command=self.translate_text,
            relief="flat",
            cursor="hand2"
        )
        translate_btn.pack(side="left", padx=10)

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

        # Привязываем Enter к переводу
        self.root.bind('<Return>', lambda e: self.translate_text())



if __name__ == "__main__":
    root = tk.Tk()
    app = Translators(root)

    # Центрируем окно
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()+150
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()