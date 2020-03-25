#!/usr/bin/env python3
#!/usr/bin/env node
import os, fileinput, sys, subprocess
from os import path, listdir
from shutil import copyfile

def executeThis(coso):
    proc = subprocess.Popen(['/bin/bash', '-i', '-c', coso])
    proc.communicate()
    exit_code = proc.wait()
    if exit_code != 0:
        print(coso + " FAILED")

os.system('')
os.chdir("..")#salimos de la carpeta inicial de montajeapps(conflictos a la hora de hacer push)
verFileDir = str(os.getcwd()) + "/montajeAPPs/versiones/inga"
if path.exists( str(os.getcwd()) + "/fe-ingaApp" )==False:
    os.system('git clone https://gitlab.vipera.com/santander-lab/fe-ingaApp.git')
    os.chdir("fe-ingaApp")
else:
    os.chdir("fe-ingaApp")
    os.system('git stash')
    os.system('git pull')


if str(sys.argv[1]) == "pre":
    os.system('git checkout preprod')

if str(sys.argv[1]) == "stg":
    os.system('git checkout release')

verFile = open(verFileDir)#close the verFile plz

dependencias = []
for i in verFile:
        dependencias.append(i[0:-1])

verFile.close()#close the verFile plz

print("NVM USE NODE--------------------------------------")
executeThis('nvm use node')

print("NVM INSTALL " + dependencias[0].split(" ")[1] + "--------------------------------------")
executeThis( 'nvm install ' + dependencias[0].split(" ")[1] )

dependencias.pop(0)
for i in dependencias:
    if i != "":
        print("NPM INSTALL -g "  + i.split(" ")[0] + "@" +  i.split(" ")[1] + "--------------------------------------")
        executeThis( 'nvm use 10.9 | npm install -g ' + i.split(" ")[0] + "@" +  i.split(" ")[1] )

print("./INSTALL.sh-------------------------------")

executeThis('nvm use 10.9 | ionic cordova prepare ios --no-interactive --confirm')
executeThis('nvm use 10.9 | ionic cordova prepare android --no-interactive --confirm')
executeThis('nvm use 10.9 | ionic cordova prepare browser --no-interactive --confirm')
executeThis('nvm use 10.9 | npm i')

print("COMANDOS EXTRA-------------------------------")
executeThis('nvm use 10.9 | ionic cordova plugin add cordova-plugin-firebase-analytics')
executeThis('nvm use 10.9 | npm install @ionic-native/firebase-analytics')
executeThis('nvm use 10.9 | ionic cordova plugin add cordova-plugin-app-version')
#ionic cordova plugin add cordova-plugin-iroot --save

print("Copiando firebase files....")
if (str(sys.argv[1]) == "pre" ): 
    firebaseDIR = os.getcwd() + "/Firebase/PRE_ENDPOINT/"
else:
    firebaseDIR = os.getcwd() + "/Firebase/STAGE_ENDPOINT/"

copyfile( firebaseDIR + "google-services.json", os.getcwd() + "/google-services.json" )
copyfile( firebaseDIR + "GoogleService-Info.plist", os.getcwd() + "/GoogleService-Info.plist" )

print("Modificando config.xml && enviroment.ts....")
if (str(sys.argv[1]) == "pre" ): 
    os.system( "sed -i -e 's/.dev././g' config.xml" )
    os.system( "sed -i -e 's/test/preprod/g' src/enviroments/enviroment.ts" )
else:
    os.system( "sed -i -e 's/.dev./.stg./g' config.xml" )
    os.system( "sed -i -e 's/test/stage/g' config.xml" )

executeThis('nvm use 10.9 | ionic cordova prepare android ios')

print("Finished!")


#os.replace("os.getcwd()" + , "path/to/new/destination/for/file.foo")
