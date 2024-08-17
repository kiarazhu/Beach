import sqlite3
connection = sqlite3.connect("beach.db")
cursor = connection.cursor()
print(cursor.execute("SELECT * FROM Beach;").fetchall())