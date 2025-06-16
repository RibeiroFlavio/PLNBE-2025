import json
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

def obter_significado(conceito):
    termo = conceito.replace(" ", "-")
    url = (
        f"https://pt.wikipedia.org/w/index.php?search={termo}+química+OR+bioquímica+OR+biomédica+OR+medicina+OR+medica"
        "&title=Especial:Pesquisar&profile=advanced&fulltext=1"
        "&advancedSearch-current=%7B%22fields%22%3A%7B%22or%22%3A%5B%22química%22%2C%22bioquímica%22%2C%22biomédica%22%2C%22medicina%22%2C%22medica%22%5D%7D%7D"
        "&ns0=1&ns6=1"
    )

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        resultado = soup.select_one(".mw-search-result-heading a") # link do primeiro resultado
        link_final = "https://pt.wikipedia.org" + resultado["href"] if resultado else url

        artigo = requests.get(link_final, headers=headers)
        soup_artigo = BeautifulSoup(artigo.text, "html.parser")
        paragrafo = soup_artigo.select_one("div.mw-parser-output > p")
        if paragrafo:
            frase = paragrafo.text.strip().split(".")[0] + "." # pegar a primeira frase do parágrafo
            return frase
    except:
        return None

    return None

# Carregar JSON original
with open("json_completo.json", encoding="utf-8") as f:
    conceitos = json.load(f)

# Atualizar conceitos sem significado
for c in conceitos:
    if "significado" not in c or not c["significado"].strip():
        print(f"🔎 A procurar: {c['conceito']}")
        significado = obter_significado(c["conceito"])
        if significado:
            c["significado"] = significado
            print(f"✅ -> {significado}")
        else:
            print("❌ Nada encontrado")

# Guardar novo ficheiro
with open("json_completo_atualizado.json", "w", encoding="utf-8") as f:
    json.dump(conceitos, f, ensure_ascii=False, indent=2)

print("📁 Ficheiro atualizado com sucesso!")