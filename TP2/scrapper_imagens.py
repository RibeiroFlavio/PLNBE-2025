import os
import json
import requests
from bs4 import BeautifulSoup

# Caminhos
input_json = "gloss_atualizado.json"
output_json = "gloss_atualizado_com_imagens.json"
output_dir = "imagens_wikipedia"
os.makedirs(output_dir, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

def obter_url_imagem(term):
    term = term.replace(" ", "-")
    url_pesquisa = (
        f"https://pt.wikipedia.org/w/index.php?search={term}+medical+OR+medicine+OR+medicina+OR+biochemistry+OR+biology+filemime%3Aimage%2Fjpeg"
        "&title=Especial%3APesquisar&profile=advanced&fulltext=1"
        "&advancedSearch-current=%7B%22fields%22%3A%7B%22filetype%22%3A%22image%2Fjpeg%22%2C%22or%22%3A%5B%22medical%22%2C%22medicine%22%2C%22medicina%22%2C%22biochemistry%22%2C%22biology%22%5D%7D%7D"
        "&ns0=1&ns6=1"
    )

    try:
        res = requests.get(url_pesquisa, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        link_resultado = soup.select_one(".mw-search-result-heading a")
        if not link_resultado:
            return None
        href = link_resultado["href"]
        pagina_ficheiro = "https://pt.wikipedia.org" + href
        res_img_page = requests.get(pagina_ficheiro, headers=headers)
        soup_img = BeautifulSoup(res_img_page.text, "html.parser")
        imagem_full = soup_img.select_one(".fullImageLink a")
        if imagem_full:
            url_img = imagem_full["href"]
            return "https:" + url_img if url_img.startswith("//") else url_img
        return None
    except:
        return None

# Ler os conceitos
with open(input_json, encoding="utf-8") as f:
    conceitos = json.load(f)

# Scraper e associação da imagem
for item in conceitos:
    termo_en_lista = item.get("en", [])
    if not termo_en_lista or not isinstance(termo_en_lista, list):
        continue

    termo = termo_en_lista[0].strip()
    print(f"🔎 A procurar imagem para: {termo}")
    url_imagem = obter_url_imagem(termo)

    if url_imagem:
        try:
            resposta = requests.get(url_imagem, headers=headers)
            if resposta.status_code == 200:
                nome_ficheiro = f"{termo.replace(' ', '_')}.jpg"
                caminho_relativo = os.path.join(output_dir, nome_ficheiro)
                with open(caminho_relativo, "wb") as f:
                    f.write(resposta.content)
                item["imagem"] = caminho_relativo.replace("\\", "/")  # Compatível com JSON e web
                print(f"✅ Imagem guardada: {caminho_relativo}")
        except Exception as e:
            print(f"⚠️ Falha ao descarregar: {termo}")
            item["imagem"] = None
    else:
        item["imagem"] = None
        print(f"❌ Nenhuma imagem encontrada para '{termo}'")

# Guardar novo ficheiro JSON com as imagens associadas
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(conceitos, f, ensure_ascii=False, indent=4)

print("\n📁 Ficheiro atualizado guardado em:", output_json)
