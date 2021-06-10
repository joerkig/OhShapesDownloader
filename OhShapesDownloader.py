import sys
import os
import requests
import subprocess
import zipfile
import re

ohshapes = 'http://ohshapes.com'
url = 'http://ohshapes.com/api/maps/latest/0?'
r = requests.get(url).json()
try:
    os.remove("dwnldurl.txt")
except FileNotFoundError:
    print("")
print("")
print("There are currently " + str(r['totalDocs']) + " custom maps on OhShapes.com")
print("")
input("Press any key to continue...")
for number in range(r['lastPage']+1):
    url2 = 'http://ohshapes.com/api/maps/latest/' + str(number)
    r2 = requests.get(url2).json()
    for x in r2['docs']:
        for v in x['directDownload']:
            text_file = open("dwnldurl.txt", "a")
            text_file.write(v)
            text_file.close()
        text_file = open("dwnldurl.txt", "a")
        text_file.write("\n")
        text_file.close()
with open("dwnldurl.txt", "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    r3 = requests.get(ohshapes + stripped_line)
    url4 = 'http://ohshapes.com/api/maps/detail/'
    r4 = requests.get(url4 + str(stripped_line.split("/")[2])).json()
    name = r4['key'] + ' - ' + re.sub('[^\w\-_\. ]', '',r4['metadata']['levelAuthorName']).strip() + ' - ' + re.sub('[^\w\-_\. ]', '',r4['metadata']['songName']).strip()
    try:
        print('Downloading ' + name)
        open(name + '.zip', 'xb').write(r3.content)
        print('Extracting ' + name + '.zip')
        os.mkdir(os.getcwd() + '\\' + name + '\\')
        zip = zipfile.ZipFile(name + '.zip')
        zip.extractall(os.getcwd() + '\\' + name + '\\')
        zip.close()
        os.remove(name + '.zip')
    except FileExistsError:
        print('File already exists!')
        os.remove(name + '.zip')