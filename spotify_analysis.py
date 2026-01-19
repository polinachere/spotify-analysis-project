"""
ПРОСТОЙ АНАЛИЗ SPOTIFY ДАННЫХ
Рабочий код для команды
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

print(" Начинаю анализ Spotify данных...")

# ==================== 1. ПРОВЕРКА ФАЙЛОВ ====================
print("\n1.  Проверяю файлы...")

# Сначала ищем в папке data/
file1_data = 'data/track_data_final.csv'
file2_data = 'data/spotify_data_clean.csv'

# Если нет в data/, ищем в текущей папке
file1_current = 'track_data_final.csv'
file2_current = 'spotify_data_clean.csv'

# Проверяем где файлы
if os.path.exists(file1_data) and os.path.exists(file2_data):
    file1 = file1_data
    file2 = file2_data
    print(" Файлы найдены в папке 'data/'")
elif os.path.exists(file1_current) and os.path.exists(file2_current):
    file1 = file1_current
    file2 = file2_current
    print(" Файлы найдены в текущей папке")
else:
    print(" Файлы не найдены!")
    print("\n Что делать:")
    print("   Положите в папку проекта:")
    print("   1. track_data_final.csv")
    print("   2. spotify_data_clean.csv")
    print("   Или создайте папку 'data/' и положите туда")
    exit()

# ==================== 2. ЗАГРУЗКА ДАННЫХ ====================
print("\n2.  Загружаю данные...")
try:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    print(f" Загружено: {len(df1)} старых треков и {len(df2)} новых")
except:
    print(" Ошибка! Файлы не найдены.")
    print("   Положите CSV-файлы в ту же папку")
    exit()

# ==================== 3. СМОТРИМ СТРУКТУРУ ====================
print("\n3.  Смотрю, какие столбцы есть")
print("   В первом файле:", list(df1.columns))
print("   Во втором файле:", list(df2.columns))

# ==================== 4. ОБЪЕДИНЯЕМ ДАННЫЕ ====================
print("\n4. 🔄 Объединяю данные")
# Добавляем метку эпохи
df1['эпоха'] = 'Классика (2009-2023)'
df2['эпоха'] = 'Современность (2025)'

# Объединяем
all_data = pd.concat([df1, df2], ignore_index=True)
print(f" Всего треков: {len(all_data)}")

# ==================== 5. ПРОСТОЙ АНАЛИЗ ====================
print("\n5.  Делаю простой анализ")

# Средняя популярность
if 'Popularity' in all_data.columns:
    avg_pop = all_data['Popularity'].mean()
    print(f"    Средняя популярность: {avg_pop:.1f}/100")

# Сравнение эпох
if 'Popularity' in all_data.columns and 'эпоха' in all_data.columns:
    classic = all_data[all_data['эпоха'] == 'Классика (2009-2023)']
    modern = all_data[all_data['эпоха'] == 'Современность (2025)']
    
    print(f"    Классика: {classic['Popularity'].mean():.1f}/100")
    print(f"    Современность: {modern['Popularity'].mean():.1f}/100")

# Топ артистов
print("\n6.  Ищу топ артистов")
if 'Artist' in all_data.columns and 'Popularity' in all_data.columns:
    # Группируем по артистам
    top_artists = all_data.groupby('Artist')['Popularity'].mean()
    top_artists = top_artists.sort_values(ascending=False).head(10)
    
    print("   ТОП-10 АРТИСТОВ:")
    for i, (artist, score) in enumerate(top_artists.items(), 1):
        print(f"   {i:2}. {artist:20} - {score:.1f}/100")

# Топ жанров
print("\n7.  Ищу топ жанров")
if 'Genre' in all_data.columns:
    top_genres = all_data['Genre'].value_counts().head(10)
    
    print("   ТОП-10 ЖАНРОВ:")
    for i, (genre, count) in enumerate(top_genres.items(), 1):
        print(f"   {i:2}. {genre:20} - {count:4} треков")

# ==================== 8. ПРОСТЫЕ ГРАФИКИ ====================
print("\n8.  Делаю простые графики")

# График 1: Распределение популярности
plt.figure(figsize=(10, 4))
if 'Popularity' in all_data.columns:
    plt.hist(all_data['Popularity'], bins=20, alpha=0.7, color='blue')
    plt.title('Распределение популярности треков')
    plt.xlabel('Популярность (0-100)')
    plt.ylabel('Количество треков')
    plt.grid(True, alpha=0.3)
    plt.savefig('график_популярность.png', dpi=100)
    print("    Сохранён график: график_популярность.png")

# График 2: Сравнение эпох
plt.figure(figsize=(10, 4))
if 'Popularity' in all_data.columns and 'эпоха' in all_data.columns:
    # Разделяем данные
    classic_data = all_data[all_data['эпоха'] == 'Классика (2009-2023)']['Popularity']
    modern_data = all_data[all_data['эпоха'] == 'Современность (2025)']['Popularity']
    
    # Создаём бокс-плот
    plt.boxplot([classic_data, modern_data], 
                labels=['Классика', 'Современность'])
    plt.title('Сравнение популярности по эпохам')
    plt.ylabel('Популярность')
    plt.grid(True, alpha=0.3)
    plt.savefig('график_эпохи.png', dpi=100)
    print("    Сохранён график: график_эпохи.png")

# ==================== 9. СОХРАНЯЕМ РЕЗУЛЬТАТЫ ====================
print("\n9.  Сохраняю результаты")

# Сохраняем объединённые данные
all_data.to_csv('spotify_все_данные.csv', index=False, encoding='utf-8')
print("   Сохранён файл: spotify_все_данные.csv")

# Сохраняем топ артистов
if 'Artist' in all_data.columns and 'Popularity' in all_data.columns:
    top_artists_df = all_data.groupby('Artist')['Popularity'] \
        .mean() \
        .sort_values(ascending=False) \
        .head(20)
    
    top_artists_df.to_csv('топ_артистов.csv', encoding='utf-8')
    print("   ✅ Сохранён файл: топ_артистов.csv")

# Пишем отчёт
print("\n10. Пишу отчёт...")
with open('отчёт.txt', 'w', encoding='utf-8') as f:
    f.write("ОТЧЁТ ПО АНАЛИЗУ SPOTIFY ДАННЫХ\n")
    f.write("=" * 40 + "\n\n")
    f.write(f"Всего проанализировано треков: {len(all_data)}\n")
    
    if 'Popularity' in all_data.columns:
        f.write(f"Средняя популярность: {all_data['Popularity'].mean():.1f}/100\n")
    
    if 'эпоха' in all_data.columns:
        f.write(f"Классических треков: {len(classic)}\n")
        f.write(f"Современных треков: {len(modern)}\n")
    
    f.write("\nСозданные файлы:\n")
    f.write("1. spotify_все_данные.csv - все данные\n")
    f.write("2. топ_артистов.csv - топ артистов\n")
    f.write("3. график_популярность.png\n")
    f.write("4. график_эпохи.png\n")
    f.write("5. отчёт.txt - этот файл\n")

print("    Сохранён отчёт: отчёт.txt")

# ==================== 10. ИТОГ ====================
print("\n" + "="*50)
print(" АНАЛИЗ ЗАВЕРШЁН!")
print("="*50)

print("\nЧто создано:")
print("1. spotify_все_данные.csv - все данные для бота")
print("2. топ_артистов.csv - список лучших артистов")
print("3. график_популярность.png - график популярности")
print("4. график_эпохи.png - сравнение эпох")
print("5. отчёт.txt - текстовый отчёт")

print("\n Теперь можно запускать Telegram-бота!")
print("   Бот будет читать файл: spotify_все_данные.csv")

