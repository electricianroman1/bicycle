import os, json
from pymongo import MongoClient
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import re

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/dnd")
client = MongoClient(MONGO_URI)
db = client.get_default_database()

def extract_name(payload: dict) -> str:
    data_field = payload.get("data")
    try:
        if isinstance(data_field, str):
            data_parsed = json.loads(data_field)
        elif isinstance(data_field, dict):
            data_parsed = data_field
        else:
            data_parsed = {}
        name_value = (data_parsed.get("name") or {}).get("value")
        if isinstance(name_value, str) and name_value.strip():
            return name_value.strip()
    except Exception:
        pass
    return payload.get("name") or "Безымянный"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришли JSON LSS после команды /add, например:\n/add {\"data\": ... }")

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Используй: /add <LSS JSON>")
        return
    try:
        payload_text = " ".join(context.args)
        payload = json.loads(payload_text)
        doc = {
            "payload": payload,
            "name": extract_name(payload),
            "owner": str(update.effective_user.id),
            "created_at": datetime.utcnow()
        }
        res = db.sheets.insert_one(doc)
        await update.message.reply_text(f"Сохранено. ID: {res.inserted_id}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    items = db.sheets.find({"owner": str(update.effective_user.id)}).sort("created_at", -1).limit(20)
    lines = [f"{x['_id']} — {x.get('name')}" for x in items]
    await update.message.reply_text("\n".join(lines) if lines else "Пусто.")

def main():
    # Проверка токена на валидный формат '<digits>:<string>'
    token_env = os.getenv('TELEGRAM_BOT_TOKEN', '').strip()
    token_pattern = re.compile(r'^\d+:[\w-]{35,}$')
    if not token_env or token_env == 'put_your_token_here' or not token_pattern.match(token_env):
        print('Ошибка: TELEGRAM_BOT_TOKEN не задан или неверного формата. Укажи реальный токен из @BotFather в .env и перезапусти.')
        return
    token = token_env
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_cmd))
    app.run_polling()

if __name__ == "__main__":
    main()
