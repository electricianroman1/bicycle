FROM python:3.11-slim

WORKDIR /app
# Контекст билда = ./telegram_bot
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app

CMD ["python", "telegram_bot.py"]
