# Простой анализ данных Spotify (2009–2025)
# Студент: [Ваше имя]
# Группа: [Номер группы]

import pandas as pd
import matplotlib.pyplot as plt
import os

print(" Начинаю анализ данных Spotify...")

# 1. Проверяем, есть ли папка с данными
if not os.path.exists("data"):
    print("Папка 'data' не найдена! Создайте её и положите туда CSV-файлы.")
    exit()

# 2. Указываем пути к файлам
file1 = "data/track_data_final.csv"
file2 = "data/spotify_data_clean.csv"

# 3. Проверяем наличие файлов
if not os.path.exists(file1):
    print(f" Файл {file1} не найден!")
    exit()
if not os.path.exists(file2):
    print(f" Файл {file2} не найден!")
    exit()

print(" Оба файла найдены. Загружаем...")

# 4. Читаем данные
try:
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
except Exception as e:
    print(" Ошибка при чтении файлов:", e)
    exit()

print(f"Загружено: {len(df1)} треков (2009–2023) и {len(df2)} треков (2025)")

# 5. Добавляем метку эпохи
df1["эпоха"] = "Классика (2009–2023)"
df2["эпоха"] = "Современность (2025)"

# 6. Объединяем таблицы
all_data = pd.concat([df1, df2], ignore_index=True)
print(f"Всего треков после объединения: {len(all_data)}")

# 7. Анализ популярности
if "Popularity" in all_data.columns:
    avg_pop = all_data["Popularity"].mean()
    print(f"\nСредняя популярность всех треков: {avg_pop:.1f}/100")
    
    # Сравнение по эпохам
    classic_avg = all_data[all_data["эпоха"] == "Классика (2009–2023)"]["Popularity"].mean()
    modern_avg = all_data[all_data["эпоха"] == "Современность (2025)"]["Popularity"].mean()
    print(f"Средняя популярность (2009–2023): {classic_avg:.1f}/100")
    print(f"Средняя популярность (2025): {modern_avg:.1f}/100")
else:
    print(" Столбец 'Popularity' не найден — пропускаем анализ популярности.")

# 8. Топ-10 артистов по популярности
if "Artist" in all_data.columns and "Popularity" in all_data.columns:
    top_artists = all_data.groupby("Artist")["Popularity"].mean().sort_values(ascending=False).head(10)
    print("\nТОП-10 артистов по средней популярности:")
    for i, (artist, score) in enumerate(top_artists.items(), 1):
        print(f"{i}. {artist} — {score:.1f}/100")
else:
    print(" Нет столбцов 'Artist' или 'Popularity' — топ артистов не строится.")

# 9. Топ-10 жанров
if "Genre" in all_data.columns:
    top_genres = all_data["Genre"].value_counts().head(10)
    print("\nТОП-10 жанров по количеству треков:")
    for i, (genre, count) in enumerate(top_genres.items(), 1):
        print(f"{i}. {genre} — {count} треков")
else:
    print("Столбец 'Genre' не найден — топ жанров не строится.")

# 10. Сохраняем объединённые данные
all_data.to_csv("spotify_все_данные.csv", index=False, encoding="utf-8")
print("\n Результаты сохранены в файл: spotify_все_данные.csv")

# 11. График: распределение популярности
if "Popularity" in all_data.columns:
    plt.figure(figsize=(8, 5))
    plt.hist(all_data["Popularity"], bins=20, color="skyblue", edgecolor="black")
    plt.title("Распределение популярности треков")
    plt.xlabel("Популярность (0–100)")
    plt.ylabel("Количество треков")
    plt.grid(True, alpha=0.3)
    plt.savefig("график_популярность.png")
    print(" График сохранён: график_популярность.png")

# 12. График: сравнение эпох (boxplot)
if "Popularity" in all_data.columns and "эпоха" in all_data.columns:
    plt.figure(figsize=(7, 5))
    data_to_plot = [
        all_data[all_data["эпоха"] == "Классика (2009–2023)"]["Popularity"],
        all_data[all_data["эпоха"] == "Современность (2025)"]["Popularity"]
    ]
    plt.boxplot(data_to_plot, labels=["2009–2023", "2025"])
    plt.title("Сравнение популярности по эпохам")
    plt.ylabel("Популярность")
    plt.grid(True, alpha=0.3)
    plt.savefig("график_эпохи.png")
    print(" График сохранён: график_эпохи.png")

# 13. Простой текстовый отчёт
with open("отчёт.txt", "w", encoding="utf-8") as f:
    f.write("ОТЧЁТ ПО АНАЛИЗУ SPOTIFY\n")
    f.write("="*30 + "\n")
    f.write(f"Всего треков: {len(all_data)}\n")
    if "Popularity" in all_data.columns:
        f.write(f"Средняя популярность: {avg_pop:.1f}/100\n")
    f.write("\nФайлы созданы:\n")
    f.write("- spotify_все_данные.csv\n")
    f.write("- график_популярность.png\n")
    f.write("- график_эпохи.png\n")
    f.write("- отчёт.txt\n")

print("\n Отчёт сохранён: отчёт.txt")
print("\n Анализ завершён! Все результаты — в корне проекта.")