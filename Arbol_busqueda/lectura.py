import sys
from array import array
import re
from collections import namedtuple
from Bus import Bus
#ESTE FICHERO ME GARANTIZA LA LECTURA CORRECTA DE LA ENTRADA
Children = namedtuple('Children', 'stop number school')


#Leo el fichero y devuelvo la estructura de datos
def leer_fichero():

    #1 Intento leer,el fichero que le paso como primer argumento

    args = len(sys.argv) - 1
    if args != 1:
        print("numero erroneo de argumentos")
        sys.exit(-1)

    try:
        f = open(sys.argv[1],"r")
    except FileNotFoundError:

        print("No se ha encontrado el fichero ",sys.argv[1])
        sys.exit(-1)

    #2 Guardo en una lista el contenido del fichero 
    lines = f.readlines()

    #3 El fichero ya esta leido, lo cierro
    f.close()
    return lines

#Obtengo el tamanyo del grafo (numero de espacios + 1 de la primera linea)
def getSize(a):
    count = 0
    #Le quito los espacios a la izquierda, me lo tragare tabule al principio o no
    linea = a.lstrip()
    j = ' '
    for i in linea:
        #Compruebo el formato le paso la columna actual, la anterior y el indice de la columna actual
        FormatHeader(i,j,a.index(i),1)
        if i == ' ':
            count += 1
        j = i
    return count + 1

#Leo las matriz del grafo linea a linea

def LeerPosiciones(linea,indice,n):
    enteros = array('l') 
    chunks = linea.split(' ')
    #Compruebo que el numero de elementos sea el correcto

    if len(chunks) != n + 1:
        print("Formato del grafo incorrecto en la linea ",indice)
        sys.exit(-1)
    j = ' '
    for i in chunks[0]:
        k = chunks[0].index(i)
        FormatHeader(i,j,k,indice)
        j = i
    for i in range(1,n+1):
        if chunks[i] == '--' or chunks[i] == '--\n':
           enteros.append(-1)
        else:
            try:
                if int(chunks[i]) > 0:
                    enteros.append(int(chunks[i],10))
                else: 
                    print("Error Coste negativo en la linea ",indice)
                    sys.exit(-1)
            except ValueError:
                print(chunks[i] ," No es un formato valido linea ",indice)
                sys.exit(-1)
    return enteros

#Obtengo la parada correspondiente a los colegios 
def GetColegios(colegios,n):
    enteros = array('l') 
    chunks = colegios.split('; ')
    #Compruebo que la sintaxis sea correcta y si lo es devuelvo la parada del colegio
    for i in chunks:
        parada = FormatSchool(i,n)
        #Comprobamos que el numero de parada sea correcto
        if parada > n - 2 or parada < 1:
            print("Numeracion erronea")
            sys.exit(-1)
        enteros.append(parada)
  
    return enteros

#Aqui de
def GetBus(autobus,n):
     pattern = re.compile("^"r"\s*B"r"\s*:"r"\s*P[0-9]+"r"\s*[0-9]+"r"\s*$")
     coincidir = pattern.match(autobus)
     if coincidir == None:
        print("La expresion ",autobus," no es correcta en la linea ",n)
        sys.exit(-1)
    
     stop = autobus.split(' ')[1]
     
     stopid = re.search('P(.*)', stop)
     parada = int(stopid.group(1))
     capacidad = int(autobus.split(' ')[2])
     return Bus(parada,capacidad)
    
#Obtengo la posicion original de los alumnos y la devuelvo en una tupla con nombre
def GetChildren(kids,n):
    chunks = kids.split('; ')
    todos = []
    for i in chunks:
        alumnos = FormatPupils(i,n)
        todos.append(alumnos.copy())
        alumnos.clear()
    return todos
#Vamos comprobando que el formato es correcto, lo separo en cabecera, grafo(implicito en LeerValores), colegios, paradas y buses(implicito en GetBus)

#En la cabecera
def FormatHeader(i,j,k,l):
    if j == ' ' and i != 'P':
        print("Formato incorrecto en linea",l," cerca de la columna",k+1)
        sys.exit(-1)
    if (j != 'P' and j.isdigit() == False) and i.isdigit() == True:
        print("Formato incorrecto en linea",l," cerca de la columna",k+1)
        sys.exit(-1)

#En los colegios con una expresion regular
def FormatSchool(cole,n):
    pattern = re.compile("^"r"\s*C([0-9]+):"r"\s*P([0-9]+)"r"\s*$")
    coincidir = pattern.match(cole)
    if coincidir == None:
        print("La expresion ",cole," no es correcta en la linea ",n)
        sys.exit(-1)
    parada = cole.split('P')[1]
    return int(parada)

#Los jodidos chavales con una expresion regular
def FormatPupils(kids,n):
    lista = []
    pattern = re.compile("^"r"\s*P[0-9]+"r"\s*:("r"\s*[0-9]+"r"\s*C([0-9]+),"r"\s*)*"r"\s*[0-9]+"r"\s*C([0-9]+)"r"\s*$")
    coincidir = pattern.match(kids)
    if coincidir == None:
        print("La expresion ",kids," no es correcta en la linea ",n)
        sys.exit(-1)
    #Ahora tengo que devolver una lista de tuplas con nombre
    stop = re.search('P(.*)'r'\s*:', kids)
    parada = int(stop.group(1))
    valor = kids.split(':')[1]
    ocurrences = valor.split(',')
    for i in ocurrences:
        
        numero = int(i.split(' ')[1])
        escuela = i.split(' ')[2]
        lista.append(Children(parada,numero,escuela))
    return lista

    
