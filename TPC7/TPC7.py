from flask import Flask, request, render_template
import json
import re
app = Flask(__name__)

#db_file = open("../Aula4/conceitos.json")
db_file = open("conceitos_.json", encoding="latin-1")

db = json.load(db_file)
db_file.close()

@app.route("/")
def hello_world():
    return render_template("home.html")

@app.route("/conceitos")
def conceitos():
    designacoes = list(db.keys())
    return render_template("conceitos.html", designacoes=designacoes, title="Lista de Conceitos")

@app.get("/conceitos/<designacao>")
def conceito(designacao):
    if designacao in db:
        return render_template("conceito.html", designacao=designacao, descricao = db[designacao])
    else:
        return render_template("conceito.html", designacao="Erro", descricao = "Descrição não encontrada")

@app.route("/api/conceitos")
def api_conceitos():
    return db

@app.route("/api/conceitos/<designacao>")
def api_conceito(designacao):

    return {"designacao":designacao, "descricao":db[designacao]}


@app.post("/conceitos")
def adicionar_conceito():
    descricao = request.form.get("descricao")
    designacao = request.form.get("designacao")

    db[designacao] = descricao
    f_out = open("conceitos_.json", "w")
    json.dump(db,f_out, indent=4, ensure_ascii=False)
    f_out.close()
    #form data

    designacoes= list(db.keys())
    return render_template("conceitos.html",designacoes=designacoes, title="Lista de Conceitos")

@app.post("/api/conceitos")
def adicionar_conceito_api():
    #json
    data = request.get_json()
    #{"designacao":"vida", "descricao": "a vida é ..."}
    db[data["designacao"]] = data["descricao"]
    f_out = open("conceitos_.json", "w")
    json.dump(db,f_out, indent=4, ensure_ascii=False)
    f_out.close()
    #form data
    return data


def find_conceito(db,query,word_bound,case_sensitive):
    res = []
    flags = 0
    if word_bound == "on":
        pattern = r"\b(" + query + r")\b"
    else:
        pattern = r"(" + query + r")"
    if case_sensitive != "on":
        flags = re.IGNORECASE

    for designacao, descricao in db.items():
        if re.search(pattern, designacao,flags) or re.search(pattern, descricao,flags):
            bold_designacao = re.sub(pattern,r"<strong>\1</strong>",designacao, flags)
            bold_descricao = re.sub(pattern,r"<strong>\1</strong>",descricao, flags)
            res.append((designacao, bold_designacao, bold_descricao))   
    return res

@app.get("/pesquisa")
def pesquisa():
    query = request.args.get("query")
    word_bound = request.args.get("word_bound")
    case_sensitive = request.args.get("case_sensitive")

    if not query:
        return render_template("pesquisa.html", title="Pesquisa")
    
    res = find_conceito(db,query,word_bound,case_sensitive)
    return render_template("pesquisa.html", conceitos=res, query=query, word_bound=word_bound, case_sensitive=case_sensitive, title="Pesquisa")


@app.delete("/conceitos/<designacao>")
def delete_conceito(designacao):
    if designacao in db:
        f_out = open("conceitos_.json", "w")
        del db[designacao]
        json.dump(db,f_out, indent=4, ensure_ascii=False)
        f_out.close()
        return {"success": True,"message": "Conceito apagado com sucesso", "redirect_url":"/conceitos", "data":designacao}
    
    return {"success": False,"message": "O conceito não existe", "data":designacao}


@app.get("/conceitos/tabela")
def conceitos_tabela():

    return render_template("tabela.html", conceitos=db.items())




app.run(host="localhost", port=4002, debug=True)
