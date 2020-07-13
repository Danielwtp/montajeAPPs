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
os.chdir("..")#salimos de la carpeta inicial de montajeapps(conflictos a la hora de hacer clone)
verFileDir = str(os.getcwd()) + "/montajeAPPs/versiones/100cards"
if path.exists( str(os.getcwd()) + "/fe-ccmanager" )==False:
    os.system('git clone https://gitlab.vipera.com/santander-lab/fe-ccmanager.git')
    os.chdir("fe-ccmanager")
else:
    os.chdir("fe-ccmanager")


os.system('git stash')
if str(sys.argv[1]) == "pre":
    os.system('git checkout preprod_mex')
    os.system('git pull origin preprod_mex')

if str(sys.argv[1]) == "stg":
    os.system('git checkout release_mex')
    os.system('git pull origin release_mex')

verFile = open(verFileDir)#close the verFile plz

dependencias = []
for i in verFile:
        dependencias.append(i[0:-1])

verFile.close()#close the verFile plz

print("NVM USE NODE--------------------------------------")
executeThis('nvm use node')

print("NVM INSTALL " + dependencias[0].split(" ")[1] + "--------------------------------------")
nvmVer = dependencias[0].split(" ")[1]
executeThis('nvm install ' + nvmVer)


dependencias.pop(0)
for i in dependencias:
    if i != "":
        print("NPM INSTALL -g "  + i.split(" ")[0] + "@" +  i.split(" ")[1] + "--------------------------------------")
        executeThis( 'nvm use ' + nvmVer + ' | npm install -g ' + i.split(" ")[0] + "@" +  i.split(" ")[1] )

print("./ENV_INSTALL.sh-------------------------------")

executeThis('nvm use ' + nvmVer + ' | npm cache clear --force')
executeThis('nvm use ' + nvmVer + ' | ionic cordova plugin add customPlugins/backgroundmode')
executeThis('nvm use ' + nvmVer + ' | ionic cordova plugin add customPlugins/themeablebrowser')
executeThis('nvm use ' + nvmVer + ' | ionic cordova plugin add customPlugins/firebase --save --variable ANDROID_PLAY_SERVICES_TAGMANAGER_VERSION=16.0.0 --variable ANDROID_FIREBASE_CORE_VERSION=16.0.0 --variable ANDROID_FIREBASE_MESSAGING_VERSION=18.0.0 --variable ANDROID_FIREBASE_CONFIG_VERSION=17.0.0 --variable ANDROID_FIREBASE_PERF_VERSION=17.0.0 --variable ANDROID_FIREBASE_AUTH_VERSION=17.0.0')
executeThis('nvm use ' + nvmVer + ' | npm install @types/lodash@ts2.2 --save')
executeThis('nvm use ' + nvmVer + ' | ionic cordova prepare ios --no-interactive --confirm')
executeThis('nvm use ' + nvmVer + ' | ionic cordova prepare android --no-interactive --confirm')
executeThis('nvm use ' + nvmVer + ' | ionic cordova prepare browser --no-interactive --confirm')
executeThis('nvm use ' + nvmVer + ' | npm i')

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
    os.system( "sed -i -e 's/DEV_ENDPOINT/PRE_ENDPOINT/g' config/config.json" )
else:
    os.system( "sed -i -e 's/.dev./.stg./g' config.xml" )
    os.system( "sed -i -e 's/DEV_ENDPOINT/STAGE_ENDPOINT/g' config/config.json" )

executeThis('nvm use ' + nvmVer + ' | ionic cordova prepare android ios && ionic cordova prepare android ios')

print("Finished!")


#os.replace("os.getcwd()" + , "path/to/new/destination/for/file.foo")
