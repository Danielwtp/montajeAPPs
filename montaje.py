#!/usr/bin/env python3
import os, sys
from os import path, listdir


#Check de parametros.
dir = os.getcwd() + "/versiones/"
proyectos = "["
for i in listdir(dir):
        proyectos += i + ", "

if len(sys.argv) != 3:
    print("./script.py " + proyectos[0:-2]  + "] [pre, stg]")
    exit(1)

if path.exists(dir+str(sys.argv[1]))==False:
    print("./script.py " + proyectos[0:-2]  + "] [pre, stg]")
    exit(1)

if (str(sys.argv[2]) != "pre" and str(sys.argv[2]) != "stg"):
    print("./script.py " + proyectos[0:-2]  + "] [pre, stg]")
    exit(1)

#Check de versiones.
name = input("Ha cambiado alguna version de "+ str(sys.argv[1]) +"?(y/N)\n")
while (name != "" and name != "y" and name != "n" and name != "Y" and name != "N"):
    name = input("Presiona y(si) or n(no) por favor\n")



numero = 0
dependencias = []
if name == "y":
    file = open(dir+str(sys.argv[1]))#close the file plz
    file2 = open(dir+str(sys.argv[1]) + ".tmp", "w+")
    print("Cuales?:(Escribe los numeros separados por espacios.)")
    for i in file:
        print(str(numero) + ": " + i[0:-1])
        dependencias.append(i[0:-1])
        numero += 1
    file.close()
    ids = input()
    for j in ids: 
        if j != " ":
            if int(j[0]) > len(dependencias)-1 or not(j.isdigit()):
                print(j+" no es a ninguna de las dependencias")
            version = input("Cual es la nueva version de " + dependencias[int(j[0])].split(" ")[0] + "?\n")
            for n in version.split("."):
                while n.isdigit() == False:
                    print(version + ": No es una numero valido.")
                    file.close()
                    exit(1)
            dependencias[int(j[0])] = dependencias[int(j[0])].split(" ")[0] + " " + version
    for i in dependencias:
        file2.write(i + "\n")
    file2.close()
    os.remove(dir+str(sys.argv[1]))
    os.rename(dir+str(sys.argv[1]) + ".tmp", dir+str(sys.argv[1]))
os.system( 'python3 ' + os.getcwd()+"/scripts/"+str(sys.argv[1]) + '.py ' + str(sys.argv[2]) )
