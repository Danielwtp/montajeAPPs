#!/usr/bin/env python3

import os, sys, subprocess

def executeThis(coso):
    proc = subprocess.Popen(['/bin/bash', '-i', '-c', coso])
    proc.communicate()
    if proc.wait() != 0:
        print(coso + " FAILED")

os.chdir("..")#salimos de la carpeta inicial de montajeapps(conflictos a la hora de hacer push)
verFileDir = str(os.getcwd()) + "/montajeAPPs/versiones/selectAll"
res=os.path.exists(str(os.getcwd()) + "/fe-select" )#Pa saber si el proyecto estaba antes.
if not res:
    os.system('git clone git@gitlab.vipera.cloud:santanderlab/sanlab-select/fe-select.git')
    os.chdir("fe-select")
else:
    os.chdir("fe-select")

os.system('git stash')
if str(sys.argv[1]) == "pre":
    os.system('git checkout preprod')
    os.system('git pull origin preprod')

if str(sys.argv[1]) == "stg":
    os.system('git checkout release')
    os.system('git pull origin release')

verFile = open(verFileDir)#close the verFile plz
dependencias = []
for i in verFile:
        dependencias.append(i[0:-1])

verFile.close()#close the verFile plz

print("NVM USE NODE--------------------------------------")
executeThis('nvm use node')
print("NVM INSTALL " + dependencias[0].split(" ")[1] + "--------------------------------------")
nvmVer = dependencias[0].split(" ")[1]
executeThis( 'nvm install ' + nvmVer )
dependencias.pop(0)

if not res:
    for i in dependencias:
        if i != "":
            print("NPM INSTALL -g "  + i.split(" ")[0] + "@" +  i.split(" ")[1] + "--------------------------------------")
            executeThis( 'nvm use ' + nvmVer + ' | npm install -g ' + i.split(" ")[0] + "@" +  i.split(" ")[1] )
    
    print("Adding platforms------------------------------------------------------------")
    executeThis('nvm use ' + nvmVer + ' | ionic cordova platform add ios --no-interactive --confirm')
    executeThis('nvm use ' + nvmVer + ' | ionic cordova platform add android --no-interactive --confirm')
    executeThis('nvm use ' + nvmVer + ' | npm i')

executeThis('nvm use ' + nvmVer + ' | ionic cordova prepare android ios --no-interactive --confirm')

print("Finish!")


#os.replace("os.getcwd()" + , "path/to/new/destination/for/file.foo")
