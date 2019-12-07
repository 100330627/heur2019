import sys
from array import array
import re
from collections import namedtuple
from Bus import Bus
import pdb
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

    FormatHeader(a)
    #Divido por el numero de espacios
    chunks = a.split()
    
    return len(chunks)

#Leo las matriz del grafo linea a linea

def LeerPosiciones(linea,indice,n):
    enteros = array('l') 
    chunks = linea.split()
    #Compruebo que los elementos tengan el formato correcto y los meto al array

    for i in chunks:
        if chunks.index(i) != 0:
            pattern = re.compile("^([0-9]+|--)$")
        else:
            pattern = re.compile("^P([0-9])+")
        coincidir = pattern.match(i)
        #En caso de que el formato no sea el adecuado
        if coincidir == None:
            print("Error en la expresion ",i," en la linea ",linea)
            sys.exit(-1)
        try:
           pos = int(i)
        except ValueError:
            pos = -1
        enteros.append(pos)

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
def FormatHeader(a):
    pattern = re.compile("^("r"\s*P([0-9]+)"r"\s*)+$")
    coincidir = pattern.match(a)
    if coincidir == None:
        print("La expresion ",a," no es correcta en la cabecera")
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

    
