from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"

# load the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

# prepare the model input

def gpt(prompt):
    messages = [
        {"role": "system", "content": """Ты — ИИ-агроном. Анализируй входные данные с датчиков и прогноз погоды.

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
    - Если вмешательство не требуется, ответь: \"Без действий\".
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
    - Без действий"""},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    # conduct text completion
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=32768
    )
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

    # parsing thinking content
    content = tokenizer.decode(output_ids, skip_special_tokens=True).strip("\n")

    return content