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




@app.route('/', methods=["get"])
def home():
  connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
  )


  cursor = connection.cursor()
  


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
        


@app.route('/process', methods=["POST"])
def process():
  connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
  )


  cursor = connection.cursor()
  
  if request.form['info'] == 'cadastrar':
    
    preco = request.form['valor']
    preco = float(preco.replace(',', '.'))
    sql_insert_Query = "INSERT INTO cotacao.cotacao (price, input_date) VALUES (%s, %s)"
    data_to_insert = (preco,datetime.now()) 
    cursor.execute(sql_insert_Query, data_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('home'))
  
  elif request.form['info'] == 'deletar':
    id = request.form['id']
    sql_insert_Query = "DELETE FROM cotacao.cotacao where id = %s"
    
    data_to_insert = (id,) 
    cursor.execute(sql_insert_Query, data_to_insert)
    connection.commit()
    return redirect(url_for('home'))
  
  elif request.form['info'] == 'atualizar':
    id = request.form['id']
    preco = request.form['valor']
    preco = float(preco.replace(',', '.'))
    sql_insert_Query = "UPDATE cotacao.cotacao SET price = %s, input_date = %s WHERE id = %s"
    data_to_insert = (preco,datetime.now(),id) 
    cursor.execute(sql_insert_Query, data_to_insert)
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('home'))
  

@app.route('/update', methods=["POST"])
def update():
  id = request.form['id']
  preco = request.form['preco']
  preco = float(preco.replace(',', '.'))
  return render_template('update.html', id=id,preco=preco)

    


if __name__ == '__main__':
    app.run(debug=True)

