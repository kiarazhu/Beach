import copy
from operator import contains

from flask import Flask, render_template, request
import sqlite3
import jinja2
app = Flask(__name__)


def queryBeach(searchTerm):
    query = f"SELECT DISTINCT location, life_guard_service  FROM Beach WHERE location LIKE '%{searchTerm}%';"
    connection = sqlite3.connect("beach.db")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    return result


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', message = "")

@app.route("/searchTab")
def switchToSearch():
    print("a")
    return render_template('search.html')
@app.route('/search', methods = ['POST'])
def search():
    print(request.form['query'])
    searchTerm = request.form['query']
    result = queryBeach(searchTerm)

    return render_template('search.html', searchResult = copy.deepcopy(result), tabIndex = 'Tab2')


    #html_table = "<table><tr><th>Location</th><th>Lifeguard Information</th></tr>"
    #for row in result:
    #    html_table+="<tr><td>"
    #    html_table+=row[0] + "</td>"
    #    html_table+="<td>" + row[1] + "</td></tr>\n"
    #html_table+="</table>\n"
    #print(html_table)
    #html = ""
    #adding_table=False
    #with open("templates/index.html", mode="r") as htmlfile:
    #    for line in htmlfile:
    #        if not adding_table:
    #            html += line
    #        if line.find("<!--start table-->")!=-1:
    #            html+=html_table
    #            adding_table=True
    #        if line.find("<!--end table-->")!=-1:
    #            adding_table=False
    #            html+="\n <!--end table--> \n"
    #write_file = open("templates/index.html", "w")
    #write_file.write(html)
    #write_file.close()
    #return html


if __name__ == '__main__':
    app.run()

