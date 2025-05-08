
def ex1(s):
    s_rev=s[::-1]
    return s_rev

def ex2(s):
    count=0
    for i in s:
        if i=="a" or i=="A":
            count=count+1
    return count

def ex3(s):
    count=0
    vogais=["a","e","i","o","u"]
    s=s.lower()
    for i in s:
        if i in vogais:
            count=count+1
    return count

def ex4(s):
    s=s.lower()
    return s

def ex5(s):
    s=s.upper()
    return s

def ex6(s):

        if s[::1] == s[::-1]:
            print("capicua")
        else: print("nao capicua")

def ex7(s1,s2):
    lista_s1=[]
    lista_s2=[]

    for i in s1:
        if i not in lista_s1:
            lista_s1.append(i)

    for i in s2:
        if i not in lista_s2:
            lista_s2.append(i)


    lista_s1.sort()
    lista_s2.sort()
    print(lista_s1, lista_s2)


    if lista_s1==lista_s2:
        print("balanceadas")
    else: print("uh oh:(")


def ex8(s1,s2):
    s1=s1.lower()
    s2=s2.lower()
    print(s2.count(s1))

def ex9(s1,s2):
    s1=s1.lower()
    s2 = s2.lower()
    s1=sorted(s1)
    s2=sorted(s2)



    if s1 == s2:
        #print("true")
        return True
    else:

        #print("false")
        return False

def ex10(dicionario):
    lista_t=[]
    lista_f=[]


    for t,f in dicionario.items():
        t=t.lower()
        lista_t.append(t)

        if type(f) == list:
            for a in f:
                a = a.lower()
                lista_f.append(a)

        else:
            f = f.lower()
            lista_f.append(f)


    for i in lista_t:
        res = []
        for j in lista_f:
                if ex9(i,j) ==True:
                        res.append(j)

        if len(res) !=0:
            print("anagrama " + str(i) +" = "+str(res))



dicionario = {
    "floresta": ["trapo", "porta", "patro"],
    "amor": [ "roma", "mora"],
    "arco": "carro",
    "velocidade": ["caso", "saco","cora"],
    "sol": ["laranja"],
    "saudacao": ["ola", "mundo"],
    "planeta": ["terra", "arte"],
    "oceano": ["onda", "mare"],
    "magia": ["chama", "macha"],
    "sombra": ["noite", "luz"]
}

ex10(dicionario)