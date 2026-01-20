
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("🤖 Spotify Bot запускается...")

# 1. Загружаем данные
df = pd.read_csv('spotify_данные.csv')

# 2. Команда /top
async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Просто показывает топ"""
    
    # Топ артистов
    top_artists = df.groupby('artist_name')['track_popularity'].mean()
    top_artists = top_artists.sort_values(ascending=False).head(5)
    
    message = "🏆 ТОП-5 АРТИСТОВ:\n\n"
    for i, (artist, score) in enumerate(top_artists.items(), 1):
        message += f"{i}. {artist}\n   Рейтинг: {score:.1f}/100\n\n"
    
    # Топ треков  
    top_tracks = df.nlargest(5, 'track_popularity')
    message += "🎵 ТОП-5 ТРЕКОВ:\n\n"
    
    for i, row in top_tracks.iterrows():
        track = row['track_name'][:20] + "..." if len(row['track_name']) > 20 else row['track_name']
        message += f"{i+1}. {track}\n   {row['artist_name']} - {row['track_popularity']}/100\n\n"
    
    await update.message.reply_text(message)

# 3. Команда /help  
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Помощь"""
    await update.message.reply_text(
        "📋 Команды:\n"
        "/top - Показать топ артистов и треков\n"
        "/help - Эта справка"
    )

# 4. Запуск бота
def main():
    # ⚠️ КАЖДЫЙ РАЗРАБОТЧИК ВСТАВЛЯЕТ СВОЙ ТОКЕН!
    TOKEN = "8579238920:AAEyilXpNUwwmY6uXRgx0nmnu6jDTQrOjPM"
    
    app = Application.builder().token(TOKEN).build()
    
    # Всего 2 команды
    app.add_handler(CommandHandler("top", top_command))
    app.add_handler(CommandHandler("help", help_command))
    
    print(f"✅ Бот готов! Запускаю...")
    app.run_polling()

if name == "__main__":

    main()

