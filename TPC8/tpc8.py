import time
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import json
from selenium import webdriver

def get_doenca_info(url_href):
    url_doenca = "https://www.atlasdasaude.pt" + url_href 
    response = requests.get(url_doenca)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    div_content = soup.find("div", class_="node-doencas")
    return {"url": url_doenca, "content": str(div_content)}

def doencas(letra):
    url = "https://www.atlasdasaude.pt/doencasaaz/" + letra
    #print(url)
    response = requests.get(url)

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    doencas = []
    for div_row in soup.find_all("div", class_="views-row"):
        designacao = div_row.div.h3.a.text.strip()
        doencas.append(designacao)


            
    return doencas

lista_doencas=[]
for a in range(ord("a"), ord("z") + 1):
    letra = chr(a)
    lista_doencas.append(doencas(letra))

#print(lista_doencas)

    
def tpc(doenca):
    doenca_link = doenca.replace(" - ", "-")
    doenca_link = doenca_link.replace(" ", "-").lower()
    doenca_link = doenca_link.replace('-à-', '-')
    doenca_link = doenca_link.replace('”','')
    doenca_link = doenca_link.replace('“', '')
    doenca_link = doenca_link.replace(',', '')
    doenca_link = doenca_link.replace('(', '')
    doenca_link = doenca_link.replace(')', '')


    if doenca =="Halitose e Alteração do Paladar": #pessimo design
        doenca_link="halitose"

    elif doenca =="Hemofilia A e B": #pessimo pessimo design
        doenca_link="hemofilia-e-b"




    urls = [
        f"https://www.atlasdasaude.pt/content/{doenca_link}",
        f"https://www.atlasdasaude.pt/content/{doenca_link}-0",
        f"https://www.atlasdasaude.pt/{doenca_link}-causas-sintomas-tratamento",
        f"https://www.atlasdasaude.pt/{doenca_link}-causas-sintomas-diagnostico-tratamento",
        f"https://www.atlasdasaude.pt/publico/content/{doenca_link}"

    ]

    for url_doenca in urls:
        if doenca == "Hepatite A": # pessimo pessimo pessimo design
            url = "https://www.atlasdasaude.pt/content/hepatite-0"
            response = requests.get(url)
            break

        response = requests.get(url_doenca)
        if response.status_code == 200:
            break



    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    div_content= soup.find_all("div", class_= "field-item even")



    titulos = div_content[1].find_all(["h2","h3"])

    dic={}
    paragrafos = []
    abstract=[]

    dic["Doenca"] = doenca
    #abstract inicial
    for par in div_content[1].children:
        if par.name in ["h2","h3"]:
            break
        else:

            abstract.append(par.text.strip())

    sec=''
    for par in abstract:
        sec = sec + par

    dic["Abstract"] = sec
 ######


    for indice, titulo in enumerate(titulos):

        #titulo = titulo.text.strip()
        if titulo.text.strip() =="Artigos relacionados":
            break


        for sibling in titulos[indice].find_next_siblings():

            if sibling.name == 'h2' or sibling.name == 'h3':

                if any(isinstance(par, list) for par in paragrafos): #verifica se no paragrafos existe alguma lista de pontos por exemplo sintomas
                    dic[titulos[indice].text.strip()] = paragrafos
                else:
                    sec = ""
                    for par in paragrafos:
                        sec += par
                    dic[titulos[indice].text.strip()] = sec
                paragrafos = []
                break

            if sibling.name == 'p' :
                paragrafos.append(sibling.text.strip())

            elif sibling.name == 'ul': #manter os sintomas como lista
                lista=[]
                for ponto in sibling.find_all('li'):
                    lista.append(ponto.text.strip())

                paragrafos.append(lista)

    '''
    for i in dic.keys():
        sec=""
        for par in dic[i]:

            
            if type(par) is list:
                
                for ponto in par:
                    sec+=str(ponto)
            else:
                sec= sec + par

        dic[i]=sec

    for i in dic.keys():
        print(f"\n{i}\n\n{dic[i]}")
'''



    return dic




lista_tpc=[]
for lista in lista_doencas:
    for doenca in lista:
        print(doenca)
        dic=tpc(doenca)
        #time.sleep(1)
        lista_tpc.append(dic)

f_out = open("tpc.json", "a", encoding="utf-8")

json.dump(lista_tpc, f_out, indent=4, ensure_ascii=False)

