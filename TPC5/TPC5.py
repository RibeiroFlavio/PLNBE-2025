import json

from flask import Flask, request, render_template
import json
app =Flask(__name__)

db_file=open("./conceitos.json", encoding ="utf8")
db= json.load(db_file)
db_file.close

@app.route("/")

def hello_world():
        return "<p>Hello, world</p>"



@app.route("/api/conceitos")
def api_conceitos():
        return db


###########TPC

@app.route("/conceitos")
def conceitos():
        designacoes = list(db.keys())
        return render_template("conceitos.html", conceitos = designacoes, title="lista de conceitos")

@app.route("/conceitos/<designacao>")
def descricoes(designacao):
        descricao = db.get(designacao)
        return f"<b>{designacao}</b> <p> {descricao} <p>"

##############TPC

@app.route("/api/conceitos/<designacao>")
def api_conceitosss(designacao):
        return {"designacao":designacao, "descricao":db[designacao]}

@app.post("/api/conceitos")
def adicionar_conceito():
        data=request.get_json()
        #
        #{"desi": "", "desc":""}
        db[data["designacao"]]= data["descricao"]
        f_out = open("conceitos_.json", "w")
        json.dump(db,f_out,indent=4, ensure_ascii=False)
        #form data
        return data


###TPC



app.run(host="localhost", port=4002, debug=True)
