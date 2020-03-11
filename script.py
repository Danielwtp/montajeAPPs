#!/usr/bin/env python3
import os, fileinput, sys
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
while (name != "" and name != "y" and name != "n"):
    name = input("Presiona y(si) or n(no) por favor\n")

file = open(dir+str(sys.argv[1]))#close the file plz

numero = 0
dependencias = []
if name == "y":
    print("Cuales?:(Escribe los numeros separados por espacios.)")
    for i in file:
        print(str(numero) + ": " + i[0:-1])
        dependencias.append(i[0:-1])
        numero = numero + 1
    ids = input()
    for j in ids: 
        if j != " " and j.isdigit():
            if int(j[0]) >= numero:
                print(j+" no pertenece a ninguna de las dependencias")
                file.close()
                exit(1)
            version = input("Cual es la nueva version de " + dependencias[int(j[0])].split(" ")[0] + "?\n")
            for n in version.split("."):
                if n.isdigit() == False:
                    print(version + ": No es una version valida.")
                    file.close()
                    exit(1)
            dependencias[int(j[0])] = dependencias[int(j[0])].split(" ")[0] + version


        