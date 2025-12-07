import MySQLdb

conn = MySQLdb.connect(
    host="127.0.0.1",
    user="root",
    passwd="kabeyi123"
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS django_blog_db;")
print("Database created or already exists.")
