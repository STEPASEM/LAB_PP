import pandas as pd

print("ЗАГРУЗКА ДАННЫХ...")
df = pd.read_csv("hf://datasets/Pablinho/movies-dataset/9000plus.csv")

print(f"Размер датасета: {df.shape}")
print(f"Колонки: {df.columns.tolist()}")

# Предобработка данных
print("\nПредобработка данных...")