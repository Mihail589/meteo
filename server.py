from flask import Flask, jsonify, request, render_template
from utilitis import sql, smerti
from flask_cors import CORS
import json
from time import sleep as s
from sql import sql 
from serial import Serial
from datetime import datetime
app = Flask(__name__)
CORS(app)
db = sql("192.168.0.13", password="123", dbname="meteo")
#printer = Serial("/dev/ttyS0", 9600)
#hc = Serial("/dev/ttyUSB0", 9600)

@app.route("/api/update", methods = ["GET"])
def api_update():
    hc.write("1,0".encode())
    data = hc.readline().decode().split(",")
    printer.write(f"ID: {data[0]}\nAir temp: {data[1]}\nAir hum: {data[2]}\nPress: {data[3]}\n".encode())
    s(1)
    printer.write(f"Soil Temp: {data[4]}\nSoil Hum: {data[5]}\nIs rain: {data[6]}\nLight: {data[7]}\n".encode())
    #ai = gpt.gpt(f"Air temp: {data[1]} Air hum: {data[2]} Press: {data[3]} Soil Temp: {data[4]} Soil Hum: {data[5]} Is rain: {data[6]} Light: {data[7]}")
    #printer.write(ai.encode())
    datatemp = {"id":int(data[0]), "atemp": int(data[1]), "ahum": int(data[2]), "press": int(data[3]), "stemp": int(data[4]), "shum": int(data[5]), "rain": bool(data[6]), "light": int(data[7]), "ai": "Недоступно", "status": "online"}
    invite(datatemp, 590615826)
    return jsonify(datatemp)

@app.route("/api/add", methods = ["POST"])
def api_fields_add():
    data = request.get_json() 
    print(data)
    try:
        id = int(data["id"])
        db.create_record("meteo", {"id": id, "name_meteo": data["name"], "coords": json.dumps(data["polygon"]), "status": data["status"], "center": json.dumps(data["center"]), "area": data["area"], "planted": data["planted"]})

    except:

        db.create_record("meteo", {"name_meteo": data["name"], "coords": json.dumps(data["polygon"]), "status": data["status"], "center": json.dumps(data["center"]), "area": data["area"], "planted": data["planted"]})
    return jsonify({"status": "ok"})

@app.route("/")
def index():
    return render_template("web_meteo.html")

@app.route("/api/fertilizer", methods = ["POST"])
def fet():
    data = request.get_json()
    db.create_record("fertilizer", {"idf": data["fieldId"], "fertilizer": data["fertilizer"]["name"], "data": data["fertilizer"]["date"], "time": data["fertilizer"]["time"]})
    return jsonify({"status": "ok"})


def invite(com,vk_id): 
    now = str(datetime.now()) 
    db.update("meteo", com["id"], {"status": com["status"]}, "id")
    db.create_record("logs",{"meteo_id":com["id"],"datatime":now,"tempa":com["atemp"],"ahum":com["ahum"],"press":com["press"],"stemp":com["stemp"],"shum":com["shum"],"is_rain":com["rain"],"ai":com["ai"],"light":com["light"]} )
    smerti.messeges(vk_id,com)

def delete_farm(id):    
    db.delete_record_column("logs",id,"meteo_id")
    db.delete_record_column("meteo",id,"id")
    db.delete_record_column("fertilizer",id,"idf")

@app.route("/api/fields", methods = ["GET"])
def api_fields():
    data = db.r("meteo")
    feild = db.r("fertilizer")
    req = []
    processed_fields = set()
    
    # Сначала добавляем поля с удобрениями
    for i in data:
        fertilizers = []
        
        b = db.last_record("logs", i[0], "meteo_id")
        if b:
            datas = {"temp": b[3], "humidityAir": b[4], "pressure": b[5], "soilMoisture": b[6], "soilTemp": b[7], "light": b[10], "rain": b[8]}
        else:
            datas = {}
        for a in feild:
            if a[1] == i[0]:
                fertilizers.append({"name": a[4], "date": a[2], "time": a[3]})
        if fertilizers:
            if datas != {}:
                req.append({"id": i[0], "name": i[1], "status": i[3], "polygon": json.loads(i[2]), "center": json.loads(i[4]), "area": i[5], "planted": i[6], "fertilizers": fertilizers, "sensors": datas, "ai": b[9]})
            else:
                req.append({"id": i[0], "name": i[1], "status": i[3], "polygon": json.loads(i[2]), "center": json.loads(i[4]), "area": i[5], "planted": i[6], "fertilizers": fertilizers})
            processed_fields.add(i[0])
        
    
    # Потом добавляем поля без удобрений
    for i in data:
        if i[0] not in processed_fields:
            req.append({"id": i[0], "name": i[1], "status": i[3], "polygon": json.loads(i[2]), "center": json.loads(i[4]), "area": i[5], "planted": i[6], "fertilizers": []})
    
    return jsonify(req)


@app.route("/api/delete", methods = ["DELETE"])
def api_fields_delete():
    data = request.get_json()
    print(data)
    delete_farm(data["fieldId"])
    return jsonify({"status": "ok"})

app.run("0.0.0.0", 5000, True) 