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
    return render_template('index.html', message = "")

@app.route('/search', methods = ['POST'])
def search():
    print(request.form['query'])
    searchTerm = request.form['query']
    result = queryBeach(searchTerm)
    html_table = "<table><tr><th>Location<\\th><th>Lifeguard Information<\\th><\\tr>"
    for row in result:
        html_table+="<tr><td>"
        html_table+=row[2] + "<\\td>"
        html_table+="<td>" + row[6] + "<\\td><\\tr>"
    html_table+="<\\table>"
    print(html_table)
    return html_table
    return render_template('html_table', searchReturn = result, table = html_table)


if __name__ == '__main__':
    app.run()


