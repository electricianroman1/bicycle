import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/dnd")
client = AsyncIOMotorClient(MONGO_URI)
db = client.dnd

#TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TOKEN = "7726648560:AAHKJD0qmU0y7smvbDMQb0N9pZPeNYmyOnQ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для управления листами персонажей DnD.\n"
        "Команды:\n"
        "/list — показать все листы\n"
        "/add <имя> — добавить новый лист\n"
    )


async def list_sheets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = await db.sheets.find().to_list(100)
    if not sheets:
        await update.message.reply_text("Нет сохранённых листов.")
        return
    reply = "\n".join([f"- {s['name']}" for s in sheets])
    await update.message.reply_text(f"Список персонажей:\n{reply}")


async def add_sheet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Использование: /add <имя персонажа>")
        return
    name = " ".join(context.args)
    await db.sheets.insert_one({"name": name, "data": {}})
    await update.message.reply_text(f"Лист персонажа '{name}' добавлен!")


async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_sheets))
    app.add_handler(CommandHandler("add", add_sheet))
    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(run_bot())
