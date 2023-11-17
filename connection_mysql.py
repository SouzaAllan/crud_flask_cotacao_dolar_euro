import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)

sql_select_Query = "select * from curso.curso"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)