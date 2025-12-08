import tkinter as tk

class Translator:
    def __init__(self, root):
        self.root = root
        self.root.title("ПЕРЕВОДЧИК")

if __name__ == "__main__":
    root = tk.Tk()
    app = Translator(root)
    root.mainloop()