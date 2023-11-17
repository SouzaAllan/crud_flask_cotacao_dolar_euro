import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import json
import requests as rs
from datetime import datetime



app = Flask(__name__, template_folder='template')

def req():
  link= "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL"
  r = rs.get(link)
  return r.text

def dolar(a):
  dl = json.loads(req())
  return round((a / float(dl['USDBRL']['bid'])),2)

def eur(a):
  eu= json.loads(req())
  return round((a / float(eu['EURBRL']['bid'])),2)




@app.route('/', methods=["get","post"])
def home():
  connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
  )


  cursor = connection.cursor()
  
  info = request.form.get('info')
  if info is not None and request.form.get['info'] == 'cadastrar':
    
    preco = request.form.get['valor']
    preco = float(preco.replace(',', '.'))
    sql_insert_Query = "INSERT INTO cotacao.cotacao (price, input_date) VALUES (%s, %s)"
    
    data_to_insert = (preco,datetime.now()) 
    cursor.execute(sql_insert_Query, data_to_insert)
    connection.commit()
    sql_select_Query = "select * from cotacao.cotacao order by id desc limit 5"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print(records)
    list_dict = [{'id': item[0],'preco': item[1],'usd': dolar(item[1]),'eur': eur(item[1])} for item in records]
    # Close the cursor and connection
    cursor.close()
    connection.close()
    return render_template('home.html', tasks=list_dict)
  
  elif info is not None and request.form['info'] == 'deletar':
    id = request.form['id']
    sql_insert_Query = "DELETE FROM cotacao.cotacao where id = %s"
    
    data_to_insert = (id,) 
    cursor.execute(sql_insert_Query, data_to_insert)
    connection.commit()
    sql_select_Query = "select * from cotacao.cotacao order by id desc limit 5"
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print(records)
    list_dict = [{'id': item[0],'preco': item[1],'usd': dolar(item[1]),'eur': eur(item[1])} for item in records]
    # Close the cursor and connection
    cursor.close()
    connection.close()
    return render_template('home.html', tasks=list_dict)

  else:
    sql_select_Query = "select * from cotacao.cotacao order by id desc limit 5"
    cursor.execute(sql_select_Query)
    if cursor.rowcount == 0:
      cursor.close()
      connection.close()
      return render_template('home.html', tasks="você ainda não possui registros, insira algum")
    else :
      records = cursor.fetchall()
      list_dict = [{'id': item[0],'preco': item[1],'usd': dolar(item[1]),'eur':eur(item[1])} for item in records]

      cursor.close()
      connection.close()
      return render_template('home.html', tasks=list_dict)
    
if __name__ == '__main__':
    app.run(debug=True)
