import re

#exercicio 1.1
lines = ["hello world","goodbye world","hi, hello there"]

for line in lines:
    match = re.match(r"hello", line)
    if match:
        print(f"hello encontra-se no início da frase: {line}")
    else:
        print(f"hello não se encontra no início da frase: {line}")

#exercicio 1.2
lines_2 = ["hello world","goodbye world","hi, hello there"]

for line_2 in lines_2:
    search = re.search(r"hello", line_2)
    if search:
        print (f"hello encontra-se na frase: {line_2}")
    else:
        print(f"hello não se encontra na frase: {line_2}")

#exercicio 1.3
line_3 = "Hello there! Uh, hi, hello, it's me... Heyyy, hello? HELLO!"

#find = re.findall(r"[Hh][Ee][Ll][Ll][Oo]",line_3,)
#print(find)

# OU:

find = re.findall(r'hello',line_3,re.IGNORECASE)
print(find)

#exercicio 1.4
line_4 = "Hello there! Uh, hi, hello, it's me... Heyyy, hello? HELLO!"

sub = re.sub(r"[Hh][Ee][Ll][Ll][Oo]",'*YEP*',line_4,)
print(sub)

# OU (neste caso não está a reconhecer o primeiro hello e o HELLO, tenho de ver):

#sub = re.sub(r"hello",'*YEP*',line_4,re.IGNORECASE)
#print(sub)

#exercicio 1.5
line_5 = "bananas, laranjas, maçãs, uvas, melancias, cerejas, kiwis, etc."

split = re.split(r",",line_5,0,0)

print (split)


#exercicio 2

def palavra_magica(frase):
    return (re.search(r'por favor[.?!]$',frase))


print(palavra_magica("Posso ir à casa de banho, por favor?"))
print(palavra_magica("Preciso de um favor."))
print(palavra_magica("Preciso, sim. Peço-te por favor. É de um favor."))

#exercício 3

def narcissismo(linha):
    ocorrencias = re.findall (r'eu',linha,re.IGNORECASE)
    contador = len(ocorrencias)
    return f"A palavra eu está presente {contador} vezes"


print(narcissismo("Eu não sei se eu quero continuar a ser eu. Por outro lado, eu ser eu é uma parte importante de quem EU sou."))

#exercicio 4

def troca_de_curso(linha4):
    novo_curso = 'desemprego'
    return re.sub (r'LEI',novo_curso,linha4,0,0)

print(troca_de_curso("LEI é o melhor curso! Adoro LEI! Gostar de LEI devia ser uma lei."))

#exercicio 5
#notas: \d+ dígitos uma ou mais vezes,  

def soma_string(linha5):
    numeros = re.findall(r'\d+',linha5)
    return sum (map(int, numeros))
    
print(soma_string("4,-6,2,3,8,-3,0,2,-5,1"))

#exercicio 6

def pronomes(linha6):
    return re.findall(r'eu|tu|ele|nós|vós|eles',linha6,re.IGNORECASE)

print(pronomes('EU, tu e Ele vamos ver o que nóS vamos fazer.'))

#exercicio 7

def variavel_valida(linha7):
    if re.match(r'^[a-z]\w*$',linha7, re.IGNORECASE):
        return True

print (variavel_valida('teste_1'))

#exercicio 8

def inteiros(linha8):
    return re.findall(r'-?\d+',linha8)

print (inteiros('o que são números? 1 ? -1? 20? quem sabe...'))

#exercicio 9

def underscores(linha9):
    return re.sub (r' +', '_', linha9)

print (underscores('Não és tu, sou eu. Preciso           de espaço. :P'))

#exercicio 10

def codigos_postais(lista):
    lista_ed = []
    for codigos_postal in lista:
        lista_ed.append(re.split(r'-',codigos_postal))
    return lista_ed
    
lista = ["4700-000","1234-567","8541-543","4123-974","9481-025"]
print(codigos_postais(lista))

