"""
Анализ данных Spotify (2009-2025)

"""

import pandas as pd
import matplotlib.pyplot as plt
import os

print("="*50)
print("Анализ данных Spotify")
print("="*50)

# 1. ЗАГРУЗКА ДАННЫХ
print("\n1. Загружаю данные...")

try:
    # Загружаем оба файла
    df_classic = pd.read_csv('data/track_data_final.csv')  # 2009-2023
    df_modern = pd.read_csv('data/spotify_data clean.csv') # 2025
    
    print(f"✓ Классика (2009-2023): {len(df_classic)} треков")
    print(f"✓ Современность (2025): {len(df_modern)} треков")
    
except:
    print("Ошибка! Файлы не найдены в папке 'data/'")
    exit()

# 2. ПОКАЗЫВАЕМ СТРУКТУРУ
print("\n2. Структура данных:")

print("\nКлассические треки - столбцы:")
for col in df_classic.columns:
    print(f"  • {col}")

print("\nСовременные треки - столбцы:")
for col in df_modern.columns:
    print(f"  • {col}")

# 3. ПОДГОТОВКА ДАННЫХ
print("\n3. Подготавливаю данные...")

# Добавляем метку эпохи
df_classic['эпоха'] = 'Классика (2009-2023)'
df_modern['эпоха'] = 'Современность (2025)'

# Приводим длительность к минутам
if 'track_duration_ms' in df_classic.columns:
    df_classic['длительность_мин'] = df_classic['track_duration_ms'] / 60000
    print("✓ Конвертировал длительность классики в минуты")

if 'track_duration_min' in df_modern.columns:
    df_modern['длительность_мин'] = df_modern['track_duration_min']
    print("✓ Взял длительность современности")

# 4. ОБЪЕДИНЯЕМ ВСЕ ДАННЫЕ
print("\n4. Объединяю данные...")
all_data = pd.concat([df_classic, df_modern], ignore_index=True)
print(f"✓ Всего треков: {len(all_data)}")

# 5. АНАЛИЗ ПОПУЛЯРНОСТИ
print("\n5. Анализ популярности треков:")

if 'track_popularity' in all_data.columns:
    # Средняя популярность
    avg_pop = all_data['track_popularity'].mean()
    print(f"  Средняя популярность: {avg_pop:.1f}/100")
    
    # По эпохам
    print("\n  По эпохам:")
    classic_avg = all_data[all_data['эпоха'] == 'Классика (2009-2023)']['track_popularity'].mean()
    modern_avg = all_data[all_data['эпоха'] == 'Современность (2025)']['track_popularity'].mean()
    
    print(f"  • Классика: {classic_avg:.1f}/100")
    print(f"  • Современность: {modern_avg:.1f}/100")
else:
    print("  В данных нет информации о популярности")

# 6. ТОП АРТИСТОВ
print("\n6. Топ артистов:")

if 'artist_name' in all_data.columns and 'track_popularity' in all_data.columns:
    # Группируем по артистам
    top_artists = all_data.groupby('artist_name')['track_popularity'].mean()
    top_artists = top_artists.sort_values(ascending=False).head(10)
    
    print("  Топ-10 артистов:")
    for i, (artist, score) in enumerate(top_artists.items(), 1):
        print(f"  {i:2}. {artist:20} - {score:.1f}/100")

# 7. ДЛИТЕЛЬНОСТЬ ТРЕКОВ
print("\n7. Длительность треков:")

if 'длительность_мин' in all_data.columns:
    avg_duration = all_data['длительность_мин'].mean()
    print(f"  Средняя длительность: {avg_duration:.2f} мин")
    
    # Самая длинная и короткая
    max_dur = all_data['длительность_мин'].max()
    min_dur = all_data['длительность_мин'].min()
    print(f"  • Самая длинная: {max_dur:.2f} мин")
    print(f"  • Самая короткая: {min_dur:.2f} мин")

# 8. СОЗДАНИЕ ГРАФИКОВ
print("\n8. Создаю графики...")

# График 1: Популярность
if 'track_popularity' in all_data.columns:
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.hist(all_data['track_popularity'], bins=20, color='lightblue', edgecolor='black')
    plt.title('Распределение популярности')
    plt.xlabel('Популярность (0-100)')
    plt.ylabel('Количество треков')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    classic_pop = all_data[all_data['эпоха'] == 'Классика (2009-2023)']['track_popularity']
    modern_pop = all_data[all_data['эпоха'] == 'Современность (2025)']['track_popularity']
    
    plt.boxplot([classic_pop, modern_pop], labels=['Классика', 'Современность'])
    plt.title('Сравнение эпох')
    plt.ylabel('Популярность')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('график_популярность.png', dpi=100)
    print("✓ Сохранён: график_популярность.png")

# График 2: Длительность
if 'длительность_мин' in all_data.columns:
    plt.figure(figsize=(8, 5))
    
    plt.hist(all_data['длительность_мин'], bins=30, color='lightgreen', alpha=0.7, edgecolor='black')
    plt.title('Длительность треков')
    plt.xlabel('Длительность (минуты)')
    plt.ylabel('Количество треков')
    plt.grid(True, alpha=0.3)
    
    plt.savefig('график_длительность.png', dpi=100)
    print("✓ Сохранён: график_длительность.png")

# 9. СОХРАНЕНИЕ РЕЗУЛЬТАТОВ
print("\n9. Сохраняю результаты...")

# Основной файл для бота
all_data.to_csv('spotify_данные.csv', index=False, encoding='utf-8')
print("✓ spotify_данные.csv - все данные для бота")

# Топ артистов в отдельный файл
if 'artist_name' in all_data.columns and 'track_popularity' in all_data.columns:
    top_df = all_data.groupby('artist_name')['track_popularity'] \
        .mean() \
        .sort_values(ascending=False) \
        .head(20)
    
    top_df.to_csv('топ_артистов.csv', encoding='utf-8')
    print("✓ топ_артистов.csv - список лучших артистов")

# Текстовый отчёт
with open('отчёт.txt', 'w', encoding='utf-8') as f:
    f.write("ОТЧЁТ ПО АНАЛИЗУ SPOTIFY\n")
    f.write("="*40 + "\n\n")
    f.write(f"Всего проанализировано треков: {len(all_data)}\n")
    
    if 'track_popularity' in all_data.columns:
        f.write(f"Средняя популярность: {all_data['track_popularity'].mean():.1f}/100\n")
    
    f.write("\nСозданные файлы:\n")
    f.write("1. spotify_данные.csv - для Telegram бота\n")
    f.write("2. топ_артистов.csv - рейтинг артистов\n")
    f.write("3. график_популярность.png\n")
    f.write("4. график_длительность.png\n")
    f.write("5. отчёт.txt\n")

print("\n Отчёт сохранён: отчёт.txt")
print("\n Анализ завершён! Все результаты — в корне проекта.")