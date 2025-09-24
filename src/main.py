from db import *;
print("Hello World")

db: Database = Database()
db.connect()
res = db.query("SELECT * FROM airport LIMIT 10;")
print(res)
db.disconnect()