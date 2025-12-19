import pandas as pd
from datetime import datetime

print("ЗАГРУЗКА ДАННЫХ...")
df = pd.read_csv("hf://datasets/Pablinho/movies-dataset/9000plus.csv")

print(f"Размер датасета: {df.shape}")
print(f"Колонки: {df.columns.tolist()}")

# Предобработка данных
print("\nПредобработка данных...")

# Преобразование даты
df['Release_Date'] = pd.to_datetime(df['Release_Date'], errors='coerce')
df['Release_Year'] = df['Release_Date'].dt.year
df['Release_Month'] = df['Release_Date'].dt.month

# Преобразование числовых полей
df['Popularity'] = pd.to_numeric(df['Popularity'], errors='coerce')
df['Vote_Count'] = pd.to_numeric(df['Vote_Count'], errors='coerce')
df['Vote_Average'] = pd.to_numeric(df['Vote_Average'], errors='coerce')

# Удаление строк с пропусками в ключевых полях
df_clean = df.dropna(subset=['Vote_Average', 'Vote_Count', 'Popularity', 'Release_Year'])

# Фильтрация по годам (возьмем последние 10 лет для репрезентативности)
current_year = datetime.now().year
df_recent = df_clean[df_clean['Release_Year'] >= current_year - 10]

# Агрегирование данных по годам
yearly_stats = df_recent.groupby('Release_Year').agg({
    'Vote_Average': 'mean',
    'Vote_Count': 'mean',
    'Popularity': 'mean',
    'Title': 'count'
}).reset_index()

yearly_stats = yearly_stats.rename(columns={'Title': 'Movies_Count'})

print(yearly_stats)