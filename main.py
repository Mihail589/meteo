from sql import sql 
from datetime import datetime
import utilitis.smerti as smerti 

db = sql(host="85.137.92.153", dbname="meteo", user="postgres", password="123")

def invite(com,vk_id): 
    now = str(datetime.now()) 
    db.create_record("logs",{"meteo_id":com["id"],"datatime":now,"tempa":com["atemp"],"ahum":com["ahum"],"press":com["press"],"stemp":com["stemp"],"shum":com["shum"],"is_rain":com["rain"],"ai":com["ai"],"light":com["light"]} )
    smerti.messeges(vk_id,com)

def delete_farm(id):    
    db.delete_record_column("logs",id,"meteo_id")
    db.delete_record_column("meteo",id,"id")
    db.delete_record_column("fertilizer",id,"idf")

invite({"id":1, "atemp": 22, "ahum": 33, "press": 44, "stemp": 55, "shum": 66, "rain":"True", "light": 88, "ai": "test"},591552435)
invite({"id":2, "atemp": 22, "ahum": 33, "press": 44, "stemp": 55, "shum": 66, "rain":"True", "light": 88, "ai": "test"},591552435)

