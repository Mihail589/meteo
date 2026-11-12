import os
from dotenv import load_dotenv
import requests

# Загружаем переменные из .env
load_dotenv()

# Константы из .env (с разумными значениями по умолчанию)
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_MODEL   = os.getenv("OLLAMA_MODEL", "gemma4:31b")
OLLAMA_URL     = os.getenv("OLLAMA_URL", "https://ollama.com/api/chat")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

if not OLLAMA_API_KEY:
    raise RuntimeError("OLLAMA_API_KEY не задан в .env")

SYSTEM_PROMPT = """Ты — ИИ-агроном. Анализируй входные данные с датчиков и прогноз погоды.

    Входные данные:
    - Температура воздуха (°C)
    - Влажность воздуха (%)
    - Атмосферное давление (гПа)
    - Температура почвы (°C)
    - Влажность почвы (%)
    - Освещённость (%)
    - Был ли дождь (да/нет)


    Твоя задача — дать одну краткую практическую рекомендацию по уходу за полем.

    Правила:
    - Ответ должен состоять из 2–5 слов.
    - Не объясняй причины.
    - Не используй вводные фразы и комментарии.
    - Если вмешательство не требуется, ответь: "Без действий".
    - Выбирай только наиболее важную рекомендацию.

    Возможные ответы:
    - Полить поле
    - Полив не требуется
    - Внести удобрения
    - Прополоть сорняки
    - Провести рыхление
    - Защитить от заморозков
    - Притенение не требуется
    - Проверить дренаж
    - Обработать от вредителей
    - Обработать от болезней
    - Без действий"""


def gpt(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 64,
        },
    }

    response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=OLLAMA_TIMEOUT)
    response.raise_for_status()

    data = response.json()
    content = data.get("message", {}).get("content", "").strip()

    return content


if __name__ == "__main__":
    example = (
        "Температура воздуха: 28°C, влажность воздуха: 35%, давление: 1012 гПа, "
        "температура почвы: 22°C, влажность почвы: 12%, освещённость: 80%, дождь: нет"
    )
    print(gpt(example))