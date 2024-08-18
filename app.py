import copy
from operator import contains

from flask import Flask, render_template, request
import sqlite3
import jinja2
app = Flask(__name__)
##
text = {"Chinese": ["为了安全游泳，请在旗帜之间游泳，并与朋友一起。不在超过您舒适范围的深水或波涛汹涌的水域游泳。如果不确定，可以向救生员询问有关海况的信息！",
                    "澳大利亚的海滩有标志帮助您了解是否适合游泳：",
                    "如果您在水中遇到困难可以举起手臂并从一侧挥到另一侧向救生员示意求助。",
                    "澳大利亚的海滩可能有不同种类的野生动物，其中一些可能是危险的。如果它是活的，请保持距离"],
        "English": ["To swim safely, swim between the flags, with a friend. Don’t swim in water that is deeper or rougher than you are comfortable. You can ask the lifeguards for information about the surf conditions if you are unsure!",
                    "Beaches in Australia have signs to help you understand whether it is safe to swim or not:",
                    "If you are in trouble in the water then you can signal for help from a lifeguard by raising your arm and waving it from side to side.",
                    "Australian beaches can contain different wildlife species, some of which can be dangerous. If it is alive, give it space."]}
flags = {"English": {"RedYellow": "Red & Yellow Flags: Swim between the flags. This area will be safe to swim in.",
                     "Red": "Red Flag: No Swimming.",
                     "Yellow": "Yellow Flag: Caution required. Potential hazards.",
                     "RedWhite": "Red & White Flag: Evacuate the water.",
                     "BlackWhite": "Black & White Flag: Surfcraft riding area boundary"},
         "Chinese": {"RedYellow": "红黄旗：在旗帜之间游泳。这一区域适合游泳。",
                     "Red": "红旗：禁止游泳。",
                     "Yellow": "黄旗：需要谨慎。可能存在潜在的危险。",
                     "RedWhite": "红白旗：立即撤离水域。",
                     "BlackWhite": "黑白旗：冲浪板区域边界。"}}

warnings = {"English": {"Warning": "Warning",
                        "NoSwim": "Swimming not advised",
                        "Waves": "Large waves",
                        "Stingers": "Marine stingers"},
            "Chinese": {"Warning": "Warning",
                        "NoSwim": "Swimming not advised",
                        "Waves": "Large waves",
                        "Stingers": "Marine stingers"}}
def queryBeach(searchTerm):
    query = f"SELECT DISTINCT location, life_guard_service  FROM Beach WHERE location LIKE '%{searchTerm}%';"
    connection = sqlite3.connect("beach.db")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    return result


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html',
                           text=text["English"],
                           flags=flags["English"],
                           warnings=warnings["English"])


@app.route('/switchLang', methods=['POST'])
def switch():
    print(request.form['lang'])

    return render_template('index.html',
                           text = text[request.form['lang']],
                           flags=flags[request.form['lang']],
                           warnings=warnings[request.form['lang']])


@app.route("/searchTab")
def switchToSearch():
    print("a")
    return render_template('search.html')
@app.route('/search', methods = ['POST'])
def search():
    print(request.form['query'])
    searchTerm = request.form['query']
    result = queryBeach(searchTerm)

    return render_template('index.html', searchResult = copy.deepcopy(result), tabIndex = 'Tab2',
                           text=text["English"],
                           flags=flags["English"],
                           warnings=warnings["English"]
                           )


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

