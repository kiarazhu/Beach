from flask import Flask, render_template, request
import sqlite3
app = Flask(__name__)


def queryBeach(searchTerm):
    query = f"SELECT * FROM Beach WHERE location LIKE '%{searchTerm}%';"
    connection = sqlite3.connect("beach.db")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    return result


@app.route('/')
def hello_world():  # put application's code here
    return render_template('search.html', message = "")

@app.route('/search', methods = ['POST'])
def search():
    print(request.form['query'])
    searchTerm = request.form['query']
    result = queryBeach(searchTerm)
    return render_template('search.html', message = result)


if __name__ == '__main__':
    app.run()

#POO
