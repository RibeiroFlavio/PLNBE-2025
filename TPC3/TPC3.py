import re

f = open("dicionario_medico.txt", encoding= "utf-8")
texto = f.read()
texto = re.sub(r'\f',"", texto)

texto = re.sub(r'\n\n(.+)', r'\n\n@\1', texto)
texto = re.sub(r'@(.+)\n\n@',r'@\1\n', texto)

termos = re.findall(r"@(.+)\n([^@]+)", texto)

inicio ="""
<!DOCTYPE html>
<html>
<style>
body {
    margin:0;
    height:100vh;
    display:flex;
    flex-direction: column;
    font-family: Lora;
    overflow: auto;
    background-color: white;
}
.head {
    display:flex;
    padding:7px;
    justify-content: center;
    align-items: center;
    background: linear-gradient(SeaGreen, SteelBlue);
    color:white;
    font-size:40px;
}

.subtitulo {
    margin: auto;
    padding: 10px;
    color: white;
    margin-top: 10px;
    border-radius: 5px;
    background-color: steelblue;
    margin-bottom: 40px;
    max-width: 30vw;
}

.corpo {
  background-color: WhiteSmoke;
  border-radius: 10px;
  margin: 10px;
  padding-left: 10px;
  margin-bottom: 10px;
  box-shadow: 5px 5px 10px grey;
  color: Black;
}

</style>
<div class = 'head'>
	<h3> Dicionário Médico</h3>
</div>
<div class = 'subtitulo'> Este é um dicionário médico desenvolvido na disciplina de PLNEB </div>"""

body = ''
for termo in termos:
    body += f"""
<body>
<div class = 'corpo'>
<h5 style ="font-size: 20px"> {termo[0]} </h5>
<p> {termo[1]} </p>
</div>
</body>"""

html = inicio + body

print(html)

file_out = open("aula3.html", "w")
file_out.write(html)
file_out.close()