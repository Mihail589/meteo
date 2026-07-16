import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

TOKEN = 'vk1.a.wp5chW3zD4ZspgYp77Iul9ceIwXIc8AXy_6XVhkDInPxZWpfgs5GjV2awKvUAfJH5dDWAlz5Dlz8_BKpNZGvkNBp8acxdfh2TI0JDkx2Iv26eJT2uglvFNqx5UhMvLcc_nIT63wWAHvVjWycSeSrH1C5KUBV5ddSeQAvR0NRZGz5rpPrZqDgHnJSXQ8QE_0cfne0X59X_iOHGthTjhco0A'   # сюда ваш ключ
GROUP_ID = 240146476     # сюда ID группы

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

maxAtemp = 30
minAtemp = -30

maxStemp = 30
minStemp = -30

maxShum = 30
minShum = 10




def messeges(id,data):
    alaram = []
    message = (
    f"🌿 **Данннные метеостанци ** (ID: {data['id']})\n"
    f"━━━━━━━━━━━━━━━━━━━━\n"
    f"🌡 Воздух:  {data['atemp']}°C,  влажность {data['ahum']}%\n"
    f"📈 Давление: {data['press']} мм рт.ст.\n"
    f"🌱 Почва:   {data['stemp']}°C,  влажность {data['shum']}%\n"
    f"☔️ Осадки:  {'есть' if data['rain'] else 'нет'}\n"
    f"☀️ Свет:    {data['light']}%\n"
    f"🤖 AI:      {data['ai']}"
)
    vk.messages.send(user_id=id, message=message, random_id=random.randint(1, 2**20))
    
    if data["atemp"] > maxAtemp:
        alaram = (f"⚠️ **ВНИМАНИЕ!** Температура воздуха превысила порог!\n" f"🔥 Сейчас: **{data['atemp']}°C** (порог {maxAtemp}°C)")
        vk.messages.send(user_id=id, message=alaram, random_id=random.randint(1, 2**20))
    elif data["atemp"] < minAtemp:
        alaram = (f"⚠️ **ВНИМАНИЕ!** Температура воздуха нниже порога!\n" f"❄️ Сейчас: **{data['atemp']}°C** (порог {minAtemp}°C)")
        vk.messages.send(user_id=id, message=alaram, random_id=random.randint(1, 2**20))

    if data["stemp"] > maxStemp:
        alaram = (f"⚠️ **ВНИМАНИЕ!** Температура почвы превысила порог!\n" f"🔥 Сейчас: **{data['stemp']}°C** (порог {maxStemp}°C)")
        vk.messages.send(user_id=id, message=alaram, random_id=random.randint(1, 2**20))
    elif data["stemp"] < minAtemp:
        alaram = (f"⚠️ **ВНИМАНИЕ!** Температура почвы нниже порога!\n" f"❄️ Сейчас: **{data['stemp']}°C** (порог {minStemp}°C)")
        vk.messages.send(user_id=id, message=alaram, random_id=random.randint(1, 2**20))

    if data["shum"] > maxShum:
        alaram = (f"⚠️ **ВНИМАНИЕ!** Владнность почвы превысила порог!\n" f"💦 Сейчас: **{data['shum']}°%** (порог {maxShum}°%)")
        vk.messages.send(user_id=id, message=alaram, random_id=random.randint(1, 2**20))
    elif data["shum"] < minShum:
        alaram = (f"⚠️ **ВНИМАНИЕ!** Влажность почвы нниже порога!\n" f"🏜️ Сейчас: **{data['shum']}°%** (порог {minShum}°%)")
        vk.messages.send(user_id=id, message=alaram, random_id=random.randint(1, 2**20))
                  
messeges(591552435,{"id":2, "atemp": -55, "ahum": 33, "press": 44, "stemp": -55, "shum": -66, "rain":"True", "light": 88, "ai": "test"})