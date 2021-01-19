import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="db_deteksiristi"
)

cursor = db.cursor()

db.commit()


  
cursor.execute(sql)
