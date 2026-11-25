import re

# Пороги
FROST_AIR_TEMP = 2      # °C
FROST_SOIL_TEMP = 1     # °C
SOIL_HUM_DRY = 30       # %
SOIL_HUM_WET = 85       # %
DISEASE_AIR_HUM = 85    # %
PEST_AIR_TEMP = 27      # °C
PEST_AIR_HUM = 40       # %
LOW_PRESSURE = 1000     # гПа


def gpt(prompt):
    # "Air temp: 23 Air hum: 40 Press: 1012 Soil Temp: 20 Soil Hum: 35 Is rain: 0 Light: 80"
    atemp, ahum, press, stemp, shum, rain, light = map(float, re.findall(r"-?\d+(?:\.\d+)?", prompt))

    if atemp <= FROST_AIR_TEMP or stemp <= FROST_SOIL_TEMP:
        return "Защитить от заморозков"
    if shum >= SOIL_HUM_WET:
        return "Проверить дренаж"
    if shum < SOIL_HUM_DRY:
        if rain or press < LOW_PRESSURE:
            return "Полив не требуется"
        return "Полить поле"
    if ahum >= DISEASE_AIR_HUM:
        return "Обработать от болезней"
    return "Без действий"


if __name__ == "__main__":
    data = ["1", "28.5", "35", "1012", "22", "12", "0", "80\r\n"]
    print(gpt(f"Air temp: {data[1]} Air hum: {data[2]} Press: {data[3]} Soil Temp: {data[4]} Soil Hum: {data[5]} Is rain: {data[6]} Light: {data[7]}"))