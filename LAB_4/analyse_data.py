import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

print("ЗАГРУЗКА ДАННЫХ...")
df = pd.read_csv("hf://datasets/Pablinho/movies-dataset/9000plus.csv")

print(f"Размер датасета: {df.shape}")

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

# Фильтрация по годам
current_year = datetime.now().year-3
start_year = current_year - 15
df_filtered = df_clean[(df_clean['Release_Year'] >= start_year) &
                       (df_clean['Release_Year'] < current_year)]

# Агрегирование данных по годам
yearly_stats = df_filtered.groupby('Release_Year').agg({
    'Vote_Average': 'mean',
    'Vote_Count': 'mean',
    'Popularity': 'mean',
    'Title': 'count'
}).reset_index()

yearly_stats = yearly_stats.rename(columns={'Title': 'Movies_Count'})

# ВИЗУАЛИЗАЦИЯ
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('Анализ фильмов по годам выпуска (за 15 лет)',
             fontsize=18, fontweight='bold')

# График 1: Средний рейтинг и количество фильмов по годам
years = yearly_stats['Release_Year']
ratings = yearly_stats['Vote_Average']
movie_counts = yearly_stats['Movies_Count']

# Столбцы кол-во фильмов
ax1_bar = ax1.twinx()
bars = ax1_bar.bar(years, movie_counts, alpha=0.3,
                   color='lightgreen', label='Количество фильмов')

years_smooth = np.linspace(years.min(), years.max(), 100)

ax1.plot(years, ratings, marker='o', linewidth=2.5,
         color='darkblue', markersize=8, label='Средний рейтинг (из 10)')

# Вторая ось для количества фильмов
ax1_bar = ax1.twinx()
bars = ax1_bar.bar(years, movie_counts, alpha=0.4,
                   color='lightgreen', label='Количество фильмов')

# Настройка осей
ax1.set_xlabel('Год выпуска', fontsize=12, fontweight='bold')
ax1.set_ylabel('Средний рейтинг', fontsize=12, fontweight='bold', color='darkblue')
ax1_bar.set_ylabel('Количество фильмов', fontsize=12, fontweight='bold', color='green')

# Горизонтальная линия среднего значения
mean_rating = ratings.mean()
ax1.axhline(y=mean_rating, color='red', linestyle=':', alpha=0.7,
            linewidth=1.5, label=f'Среднее: {mean_rating:.2f}')

ax1.grid(True, alpha=0.3, linestyle=':')

# Объединение легенд
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_bar.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig('movies_popularity_analysis.png', dpi=300, bbox_inches='tight')
print("\nВизуализация сохранена как 'movies_popularity_analysis.png'")
plt.show()