from utilitis import sql

db = sql.sql("85.137.92.153", password="123", dbname="meteo")
db.delete_record_column("logs",1,"meteo_id")