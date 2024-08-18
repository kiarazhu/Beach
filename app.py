import copy
from operator import contains

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)
##
text = {"Chinese": ["为了安全游泳，请在旗帜之间游泳，并与朋友一起。不在超过您舒适范围的深水或波涛汹涌的水域游泳。如果不确定，可以向救生员询问有关海况的信息！",
                    "澳大利亚的海滩有标志帮助您了解是否适合游泳：",
                    "如果您在水中遇到困难可以举起手臂并从一侧挥到另一侧向救生员示意求助。",
                    "澳大利亚的海滩可能有不同种类的野生动物，其中一些可能是危险的。如果它是活的，请保持距离"],
        "English": ["To swim safely, swim between the flags, with a friend. Don’t swim in water that is deeper or rougher than you are comfortable. You can ask the lifeguards for information about the surf conditions if you are unsure!",
                    "Beaches in Australia have signs to help you understand whether it is safe to swim or not:",
                    "If you are in trouble in the water then you can signal for help from a lifeguard by raising your arm and waving it from side to side.",
                    "Australian beaches can contain different wildlife species, some of which can be dangerous. If it is alive, give it space."],
        "German": ["Um sicher zu schwimmen, schwimmen Sie zwischen den Flaggen, zusammen mit einem Freund. Schwimmen Sie nicht in Wasser, das tiefer oder rauer ist, als es Ihnen angenehm ist. Wenn Sie unsicher sind, können Sie die Rettungsschwimmer nach den Surfbedingungen fragen!",
                   "An australischen Stränden gibt es Schilder, die Ihnen helfen zu verstehen, ob es sicher ist, zu schwimmen oder nicht:",
                   "Wenn Sie im Wasser in Schwierigkeiten geraten können Sie durch Heben und Winken Ihres Arms von einer Seite zur anderen um Hilfe signalisieren.",
                   "Australische Strände können verschiedene Wildtierarten enthalten, von denen einige gefährlich sein können. Wenn es lebt, halten Sie Abstand."],
        "French": ["Pour nager en toute sécurité, nagez entre les drapeaux, avec un ami. Ne nagez pas dans une eau plus profonde ou plus agitée que ce que vous pouvez gérer. Si vous avez des doutes, vous pouvez demander des informations aux sauveteurs sur les conditions de surf.",
                   "Les plages en Australie ont des panneaux pour vous aider à comprendre s'il est sûr de nager ou non:",
                   "En cas de problème dans l'eau Vous pouvez signaler un besoin d'aide à un sauveteur en levant le bras et en le balançant d'un côté à l'autre.",
                   "Les plages australiennes peuvent abriter différentes espèces de faune sauvage, dont certaines peuvent être dangereuses. Si elle est vivante, gardez vos distances."]

        }
flags = {"English": {"RedYellow": "Red & Yellow Flags: Swim between the flags. This area will be safe to swim in.",
                     "Red": "Red Flag: No Swimming.",
                     "Yellow": "Yellow Flag: Caution required. Potential hazards.",
                     "RedWhite": "Red & White Flag: Evacuate the water.",
                     "BlackWhite": "Black & White Flag: Surfcraft riding area boundary"},

         "French": { "RedYellow": "Drapeaux Rouge & Jaune : Nagez entre les drapeaux. Cette zone est sûre pour nager.",
                     "Red": "Drapeau Rouge : Interdiction de nager.",
                     "RedWhite": "Drapeau Rouge & Blanc : Évacuez l'eau immédiatement.",
                     "BlackWhite": "Drapeau Noir & Blanc : Limite de la zone de surf."},

         "Chinese": {"RedYellow": "红黄旗：在旗帜之间游泳。这一区域适合游泳。",
                     "Red": "红旗：禁止游泳。",
                     "Yellow": "黄旗：需要谨慎。可能存在潜在的危险。",
                     "RedWhite": "红白旗：立即撤离水域。",
                     "BlackWhite": "黑白旗：冲浪板区域边界。"},
         "German": {"RedYellow": "Rot-Gelbe Flaggen: Schwimmen Sie zwischen den Flaggen. Dieser Bereich ist sicher zum Schwimmen.",
                    "Red": "Rote Flagge: Schwimmen verboten.",
                    "Yellow": "Gelbe Flagge: Vorsicht ist geboten. Mögliche Gefahren.",
                    "RedWhite": "Rot-Weiße Flagge: Verlassen Sie sofort das Wasser.",
                    "BlackWhite": "Schwarz-Weiße Flagge: Grenze des Surfbereichs."}
         }

warnings = {"English": {"Warning": "Warning",
                        "NoSwim": "Swimming not advised",
                        "Waves": "Large waves",
                        "Stingers": "Marine stingers"},
            "Chinese": {"Warning": "Warning",
                        "NoSwim": "Swimming not advised",
                        "Waves": "Large waves",
                        "Stingers": "Marine stingers"},
            "German": {"Warning": "Warnung",
                       "NoSwim": "Schwimmen nicht empfohlen",
                       "Waves": "Hohe Wellen vorhanden.",
                       "Stingers": "Gefährliche Quallen vorhanden."},
            "French": {"Warning": "Avertissement",
                       "NoSwim": "La baignade n'est pas recommandée.",
                       "Waves": "Présence de grosses vagues.",
                       "Stingers": "Présence de méduses dangereuses."}


            }

def queryBeach(searchTerm):
    query = f"SELECT DISTINCT location, life_guard_service  FROM Beach WHERE location LIKE '%{searchTerm}%';"
    connection = sqlite3.connect("beach.db")
    cursor = connection.cursor()
    result = cursor.execute(query).fetchall()
    return result


@app.route('/')
def index():  # put application's code here
    return render_template('index.html',
                           text=text["English"],
                           flags=flags["English"],
                           warnings=warnings["English"])

@app.route('/search')
def searchScreen():
    return render_template('search.html')

@app.route('/switchLang', methods=['POST'])
def switch():
    print(request.form['lang'])

    return render_template('index.html',
                           text = text[request.form['lang']],
                           flags=flags[request.form['lang']],
                           warnings=warnings[request.form['lang']])



@app.route('/search', methods = ['POST'])
def search():
    print(request.form['query'])
    searchTerm = request.form['query']
    result = queryBeach(searchTerm)

    return render_template('search.html', searchResult = copy.deepcopy(result), tabIndex = 'Tab2',
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
#app.run()
