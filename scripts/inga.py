#!/usr/bin/env python3
#!/usr/bin/env node
import os, fileinput, sys
from os import path, listdir


os.system('')
os.system('git clone https://gitlab.vipera.com/santander-lab/fe-ingaApp.git')




dir = os.getcwd() + "/versiones/"
os.chdir("fe-ingaApp")
file = open(dir+str(sys.argv[1]))#close the file plz

dependencias = []
for i in file:
        dependencias.append(i[0:-1])
print("NVM USE NODE--------------------------------------")
os.system('nvm use node')
print("NVM INSTALL " + dependencias[0].split(" ")[1] + "--------------------------------------")
os.system( 'bash nvm install ' + dependencias[0].split(" ")[1] )
os.system( 'bash nvm use ' + dependencias[0].split(" ")[1] )
dependencias.pop(0)
for i in dependencias:
    if i != "":
        print(i)
        os.system('npm install -g ' + i.split(" ")[0] + "@" +  i.split(" ")[1])
exit(0)
os.system('ionic cordova prepare ios --no-interactive --confirm')
os.system('ionic cordova prepare android --no-interactive --confirm')
os.system('ionic cordova prepare browser --no-interactive --confirm')
print("NPM I--------------------------------------")
os.system('npm i') 