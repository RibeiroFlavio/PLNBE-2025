from flask import Flask, request, render_template
from markupsafe import Markup
import copy
import html
import json
import re

app = Flask(__name__)


db_file = open("json_completo.json", encoding="utf-8")

db = json.load(db_file)
db_file.close()




associacoes_dic = {}



#dicionario de associacoes
for conceito in db:
    for key, value in conceito.items():
        match = re.match(r"outras associacoes a '(.*)'", key)
        if match:
            termo = match.group(1)
            associacoes_dic[termo] = value



#print(associacoes_dic)





def aplicar_tooltips(texto, associacoes_dict):
    for palavra, associacoes in associacoes_dict.items():
        tooltip_raw = "<br>".join(associacoes) #br é tipo um enter
        tooltip_escaped = html.escape(tooltip_raw) #dá escape a caracteres especiais

        padrao = r'(?<!["=])\b(' + re.escape(palavra) + r')\b(?![^<]*?>)' #garantir que nao estou a mexer nas outras tags da pagina html
        substituto = (
            r'<span data-bs-toggle="tooltip" data-bs-html="true" '
            f'title="{tooltip_escaped}" '
            r'style="border-bottom: 1px dotted #000;">\1</span>'
        )

        texto = re.sub(padrao, substituto, texto, flags=re.IGNORECASE)

    return Markup(texto)

def find_conceito(db, query):
    res = []
    pattern = r"(" + re.escape(query) + r")"
    flags = re.IGNORECASE

    for conceito in db:
        match_encontrado = False
        conceito_realcado = {}
        conceito_realcado["original"] = conceito.get("conceito", "")

        for campo, valor in conceito.items():
            if campo.lower() == "área médica":
                continue
            if len(campo) == 2 and campo.isalpha():
                continue  # ignora traduções

            if isinstance(valor, str):
                if re.search(pattern, valor, flags):
                    match_encontrado = True
                    conceito_realcado[campo] = re.sub(pattern, r"<strong>\1</strong>", valor, flags)
                else:
                    conceito_realcado[campo] = valor
            elif isinstance(valor, list):
                realcados = []
                for item in valor:
                    if re.search(pattern, item, flags):
                        match_encontrado = True
                        realcados.append(re.sub(pattern, r"<strong>\1</strong>", item, flags))
                    else:
                        realcados.append(item)
                conceito_realcado[campo] = realcados
            else:
                conceito_realcado[campo] = valor

        if match_encontrado:
            res.append(conceito_realcado)

    return res





@app.route("/")
def homepage():
    return render_template("home.html")

@app.get("/pesquisa")
def pesquisa():
    query = request.args.get("query", "").strip()

    if not query:
        return render_template("pesquisa_resultados.html", conceitos=[], query=query)

    resultados = find_conceito(db, query)
    return render_template("pesquisa_resultados.html", conceitos=resultados, query=query)


@app.get("/conceitos/")
def conceitos_tabela():

    return render_template("conceitos_tabela.html", conceitos=db)


@app.get("/conceitos/<designacao>")
def conceito(designacao):


    for item in db:
        if item.get("conceito").lower() == designacao.lower():

            # para não modificar o original (inicialmente depois de entrar num conceito ele aplicava essas tooltips ja carregadas nas outras paginas)
            item_copy = copy.deepcopy(item)

            campos_de_texto = [
                "contexto",
                "significado",
                "significado_enciclopédico",
                "definicao catalã"
            ]

            for campo in campos_de_texto:
                if campo in item_copy:
                    item_copy[campo] = aplicar_tooltips(item_copy[campo], associacoes_dic)

            return render_template("conceito.html", conceito=item_copy, designacao=designacao)

    return render_template("conceito.html", conceito={"conceito": "Erro", "descricao": "Conceito não encontrado"})


@app.delete("/conceitos/<designacao>")
def delete_conceito(designacao):
    for i, conceito in enumerate(db):
        if conceito.get("conceito", "").lower() == designacao.lower():
            del db[i]
            with open("json_completo.json", "w", encoding="utf-8") as f_out:
                json.dump(db, f_out, indent=4, ensure_ascii=False)
            return {
                "success": True,
                "message": "Conceito apagado com sucesso",
                "redirect_url": "/conceitos"
            }
    return {"success": False, "message": "O conceito não existe"}



@app.route("/areas")
def pag_areas():
    # lista de areas medicas unicas
    areas_medicas = []
    for conceito in db:
        if "área médica" in conceito:
            areas_medicas.append(conceito["área médica"])

    areas_medicas = list(set(areas_medicas))
    areas_medicas.sort()
    return render_template("areas.html", areas=areas_medicas)


@app.get("/areas/<area>")
def area_especifica(area):

    conceitos_area=[]

    for item in db:

        if not item.get("área médica"):
            continue
        elif item.get("área médica").lower() == area.lower():

            conceitos_area.append(item)



    return render_template("tabela_area_conceitos.html", conceitos=conceitos_area , area=area)


@app.get("/conceitos/novo")
def novo_conceito():
    return render_template("adicionar_conceito.html")

@app.post("/conceitos")
def adicionar_conceito():
    novo_conceito = {}

    campos_simples = [
        "conceito", "significado", "significado_enciclopédico",
        "contexto", "definicao catalã", "área médica", "ca"
    ]
    campos_lista = ["sinónimos pt"]

    for campo in campos_simples:
        valor = request.form.get(campo)
        if valor:
            novo_conceito[campo] = valor.strip()

    for campo in campos_lista:
        valor = request.form.get(campo)
        if valor:
            novo_conceito[campo] = [s.strip() for s in valor.split(",") if s.strip()]

    # falta o campo conceito
    if "conceito" not in novo_conceito or not novo_conceito["conceito"].strip():
        return {
            "success": False,
            "message": "Falta o campo 'conceito'."
        }

    # conceito ja existe
    conceito_lower = novo_conceito["conceito"].strip().lower()
    for item in db:
        if item.get("conceito", "").strip().lower() == conceito_lower:
            return {
                "success": False,
                "message": "O conceito já existe."
            }


    for i in range(1, 6):
        lang = request.form.get(f"trad_lang_{i}", "").strip()
        val = request.form.get(f"trad_val_{i}", "").strip()
        if lang and val:
            novo_conceito[lang] = [v.strip() for v in val.split(",") if v.strip()]

    db.append(novo_conceito)

    with open("json_completo.json", "w", encoding="utf-8") as f_out:
        json.dump(db, f_out, indent=4, ensure_ascii=False)

    return {
        "success": True,
        "message": "Conceito adicionado com sucesso.",
        "redirect_url": "/conceitos"
    }




@app.get("/conceitos/<designacao>/editar")
def editar_conceito(designacao):
    for item in db:
        if item.get("conceito", "").lower() == designacao.lower():
            conceito = item


            campos_fixos = [
                "conceito", "significado", "significado_enciclopédico",
                "contexto", "definicao catalã", "área médica", "ca", "sinónimos pt"
            ]


            regex_idioma = re.compile(r"^[a-z]{2}$", re.IGNORECASE)

            trads = []
            for chave, valor in conceito.items():
                if chave not in campos_fixos and regex_idioma.match(chave):
                    if isinstance(valor, str):
                        trads.append((chave, valor))
                    elif isinstance(valor, list):
                        trads.append((chave, valor[0]))

            return render_template(
                "atualizar_conceito.html",
                conceito=conceito,
                trads=trads,
                original_nome=designacao
            )




@app.post("/conceitos/<designacao>/atualizar")
def atualizar_conceito(designacao):
    for i, conceito in enumerate(db):
        if conceito.get("conceito").lower() == designacao.lower():
            atualizado = {}

            campos_simples = [
                "conceito", "significado", "significado_enciclopédico",
                "contexto", "definicao catalã", "área médica", "ca"
            ]
            campos_lista = ["sinónimos pt"]

            for campo in campos_simples:
                valor = request.form.get(campo)
                if valor:
                    atualizado[campo] = valor.strip()

            for campo in campos_lista:
                valor = request.form.get(campo)
                if valor:
                    atualizado[campo] = [s.strip() for s in valor.split(",") if s.strip()]

            for i_trad in range(1, 6):
                lang = request.form.get(f"trad_lang_{i_trad}", "").strip()
                val = request.form.get(f"trad_val_{i_trad}", "").strip()
                if lang and val:
                    atualizado[lang] = [v.strip() for v in val.split(",") if v.strip()]

            db[i] = atualizado

            with open("json_completo.json", "w", encoding="utf-8") as f_out:
                json.dump(db, f_out, indent=4, ensure_ascii=False)

            return {
                "success": True,
                "message": "Conceito atualizado com sucesso",
                "redirect_url": "/conceitos"
            }

            return {
                "success": False,
                "message": "Erro: conceito não encontrado"
            }



app.run(host="localhost", port=4002, debug=True)


