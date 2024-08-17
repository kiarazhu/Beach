from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('search.html', message = "aaaa")

@app.route('/search', methods = ['POST'])
def search():
    query = "SELECT * FROM Beach WHERE location LIKE %'{request.form['query']}'%;"
    #query = "SELECT * FROM Beach WHERE location LIKE %'" + "the" + "'%;"
    connection = sqlite3.connect("beach.db")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    return result


if __name__ == '__main__':
    app.run()

#POO
