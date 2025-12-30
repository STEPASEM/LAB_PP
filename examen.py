import turtle
import random
import string

# Настройка экрана
screen = turtle.Screen()
screen.title("Генератор паролей")
screen.setup(400, 300)
screen.bgcolor("white")

# Настройки
use_uppercase = True
use_numbers = True
use_special = True
password_length = 12

# Черепашка для рисования
t = turtle.Turtle()
t.hideturtle()
t.speed(0)

# Текущий пароль
current_password = ""


def draw_all():
    """Рисует все элементы"""
    t.clear()

    # Поле пароля (просто рамка)
    t.penup()
    t.goto(-150, 100)
    t.pendown()
    for _ in range(2):
        t.forward(300)
        t.right(90)
        t.forward(40)
        t.right(90)

    # Чекбоксы
    draw_checkbox(-150, 50, "A-Z", use_uppercase)
    draw_checkbox(-150, 20, "0-9", use_numbers)
    draw_checkbox(-150, -10, "!@#", use_special)

    # Поле длины (текст и цифра)
    t.penup()
    t.goto(-150, -50)
    t.write("Длина:", font=("Arial", 12))

    t.penup()
    t.goto(-100, -50)
    t.write(str(password_length), font=("Arial", 12, "bold"))

    # Кнопка создать (просто текст)
    t.penup()
    t.goto(100, -50)
    t.write("[Создать]", font=("Arial", 12))

    # Генерируем пароль
    generate_password()


def draw_checkbox(x, y, label, checked):
    """Рисует чекбокс"""
    # Квадрат
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    for _ in range(4):
        t.forward(15)
        t.right(90)
    t.end_fill()

    # Рамка
    t.penup()
    t.goto(x, y)
    t.pendown()
    for _ in range(4):
        t.forward(15)
        t.right(90)

    # Галочка
    if checked:
        t.penup()
        t.goto(x + 3, y - 10)
        t.write("✓", font=("Arial", 12))

    # Текст
    t.penup()
    t.goto(x + 20, y - 8)
    t.write(label, font=("Arial", 12))


def generate_password():
    """Генерирует пароль"""
    global current_password

    chars = "abcdefghijklmnopqrstuvwxyz"

    if use_uppercase:
        chars += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if use_numbers:
        chars += "0123456789"
    if use_special:
        chars += "!@#$%^&*"

    password = ''.join(random.choice(chars) for _ in range(password_length))
    current_password = password

    # Удаляем старый пароль
    t.penup()
    t.goto(-149, 99)  # Внутри рамки
    t.pendown()
    t.fillcolor("white")
    t.begin_fill()
    for _ in range(2):
        t.forward(298)  # Чуть меньше, чем рамка
        t.right(90)
        t.forward(38)  # Чуть меньше, чем рамка
        t.right(90)
    t.end_fill()

    # Пишем новый пароль по центру
    t.penup()
    t.goto(-140, 75)  # Выше, чтобы было по центру рамки
    t.write(password, font=("Arial", 12))


def handle_click(x, y):
    """Обрабатывает клики мыши"""
    global use_uppercase, use_numbers, use_special, password_length

    # Чекбоксы
    if -150 < x < -135:
        if 50 > y > 35:  # A-Z
            use_uppercase = not use_uppercase
            draw_checkbox(-150, 50, "A-Z", use_uppercase)
            generate_password()
        elif 20 > y > 5:  # 0-9
            use_numbers = not use_numbers
            draw_checkbox(-150, 20, "0-9", use_numbers)
            generate_password()
        elif -10 > y > -25:  # !@#
            use_special = not use_special
            draw_checkbox(-150, -10, "!@#", use_special)
            generate_password()

    # Поле длины (цифра)
    elif -100 < x < -60 and -55 < y < -35:
        # Запрашиваем новую длину
        new_len = screen.textinput("Длина пароля", f"Введите длину (4-20):\nТекущая: {password_length}")
        if new_len and new_len.isdigit():
            length = int(new_len)
            if 4 <= length <= 20:
                password_length = length
                # Обновляем отображение длины
                t.penup()
                t.goto(-100, -55)  # Начинаем левее и ниже
                t.fillcolor("white")
                t.begin_fill()
                for _ in range(2):
                    t.forward(50)  # Шире!
                    t.right(90)
                    t.forward(25)  # Выше!
                    t.right(90)
                t.end_fill()
                t.penup()
                t.goto(-100, -50)
                t.write(str(password_length), font=("Arial", 12, "bold"))
                generate_password()

    # Кнопка создать
    elif 100 < x < 170 and -50 < y < -40:
        generate_password()


# Запуск
draw_all()
screen.onclick(handle_click)
screen.mainloop()