import urllib.request, urllib.parse, urllib.error
import json
import ssl
import xml.etree.ElementTree as ET
import os
import sqlite3
import codecs
import webbrowser
import winsound
filename = 'where.html'
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second



def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
#fname = input('Enter file name: ')
fname = 'C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_pythons/Spot That Fire v.3.0 App/nasa.xml'
clear()
#if ( len(fname) < 1 ) : fname = 'Library.xml'
#if ( len(fname) < 1 ) : fname = 'comments_42.xml'
if ( len(fname) < 1 ) : fname = 'C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_pythons/Spot That Fire v.3.0 App/nasa.xml'

def lookup(d, key):
    found = False
    for child in d:
        #if found : return child.text
        if child.tag == key: #and child.text == "ON":
            return child.text

stuff = ET.parse(fname)

#print(stuff)

all = stuff.findall('table/row')
print('Records:', len(all))

registros = list()
count = 0

fhand = codecs.open('where.js', 'w', "utf-8")
fhand.write("myData = [\n")

while True:
    i = 1
    for entry in all:
        sector = lookup(entry, 'sector')
        city = lookup(entry, 'city')
        status = lookup(entry, 'status')
        lineas = str(i) + "/" + sector + "/" + city + "/" + status
        registros.append(lineas)
        #print(i, "/", sector, "/", city, "/", status)
        print(lineas)
        i = i + 1
    n = int(input("Enter record:"))
    clear()
    print(registros[n-1])
    datos = registros[n-1].split("/")
    datos1 = datos[1] + " " + datos[2]
    print("Record:", datos)
    print("Location:", datos1)

    api_key = False
    #If you have a Google Places API key, enter it here
    # api_key = 'AIzaSy___IDByT70'
    # https://developers.google.com/maps/documentation/geocoding/intro

    if api_key is False:
        api_key = 42
        serviceurl = 'http://py4e-data.dr-chuck.net/json?'
    else :
        serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    #while True:
        #address = input('Enter location: ')

    address = datos1
    print(datos1)
    if len(address) < 1: break
    parms = dict()
    parms['address'] = address
    if api_key is not False: parms['key'] = api_key
    url = serviceurl + urllib.parse.urlencode(parms)
    print('Retrieving', url)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')

    try:
        js = json.loads(data)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Failure To Retrieve ====')
        print(data)
        continue

        #lat = js['results'][0]['place_id']
        #lat = js['results'][0]['formatted_address']
    lat = js['results'][0]['geometry']['location']

    otros = js['results'][0]['address_components']
    i = len(otros)
    latitud = lat["lat"]
    longitud = lat["lng"]
    print("latitud:", latitud)
    print("longitud:", longitud)
    x = input("Any key to continue...")
    clear()
    j = 0
    
    while j < i:
        print(js['results'][0]['address_components'][j]["long_name"])
        j = j + 1
    x = input("Any key to continue")
    clear()
    fhand = codecs.open('C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_pythons/Spot That Fire v.3.0 App/where.js', 'w', "utf-8")
    fhand.write("myData = [\n")

    lat = latitud
    lng = longitud
    print(lat,lng)
    x = input("procesando..")
    # winsound.Beep(frequency, duration)
    count = count + 1
    #print('cuenta',count)
    if count > 1 : fhand.write(",\n")
    output = "["+ str(lat)+ "," + str(lng) + "]"
    fhand.write(output)
    fhand.write("\n];\n")
   
    webbrowser.open("C:/Users/USER/Desktop/Prog/PROGRAMAS/proyecto_NASA_workspace/proyecto_NASA_pythons/Spot That Fire v.3.0 App/where.html")
    fhand.close()