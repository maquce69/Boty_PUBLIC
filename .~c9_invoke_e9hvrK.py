# -*- coding: utf-8 -*-
 
import telebot # Librería de la API del bot.
from telebot import types # Tipos para la API del bot.
import random, os
import datetime
import pyjokes
import time # Librería para hacer que el programa que controla el bot no se acabe.
import sys
import urllib
import urllib2
import json
import re
import feedparser
import time
from subprocess import check_output


reload(sys) 
sys.setdefaultencoding("utf-8")

TOKEN = '148466216:AAGCWW12qa0Y17gpF8H8TeyQeoobpNfaSLc' # Nuestro tokken del bot (el que @BotFather nos dió).
administrador = 10721401 # Este es mi ID, vosotros poned el vuestro
usuarios = [line.rstrip('\n') for line in open('usuarios.txt')] # Cargamos la lista de usuarios.
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.
segdia = 86400
segsem = 604800 # Cambiar numero con los segundos que queramos que tarde en decir el mensaje

def listener(messages):
    for m in messages:
        cid = m.chat.id
        if m.content_type == 'text': # Sólo saldrá en el log los mensajes tipo texto
            if cid > 0:
                mensaje = str(m.chat.first_name) + " [" + str(cid) + "]: " + m.text # Si 'cid' es positivo, usaremos 'm.chat.first_name' para el nombre.
            else:
                mensaje = str(m.from_user.first_name) + "[" + str(cid) + "]: " + m.text # Si 'cid' es negativo, usaremos 'm.from_user.first_name' para el nombre.

            f = open( 'log.txt', 'a') # Abrimos nuestro fichero log en modo 'Añadir'.
            f.write(mensaje + "\n") # Escribimos la linea de log en el fichero.
            f.close() # Cerramos el fichero para que se guarde.
            print mensaje # Imprimimos el mensaje en la terminal, que nunca viene mal :)
        
bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.


#############################################
#Funciones
@bot.message_handler(commands=['help'])
def command_leeroperaciones(m):
    cid = m.chat.id
    scid = str(cid)
    milist= "            "
    archi=open('operaciones.txt','r')
    for linea in archi:
        milist=milist+linea
    archi.close() 
    print milist
    bot.send_message( cid, milist) 

@bot.message_handler(commands=['vacia'])
def command_vacia(m):
    cid = m.chat.id
    bot.send_message( cid,"Vamos a ello \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n Que bien me alegro por ti" )


@bot.message_handler(commands=['meneame']) 
def command_meneame(m): 
    feed = feedparser.parse('http://meneame.feedsportal.com/rss')
    cid = m.chat.id
    # print all posts
    count = 1
    blockcount = 1
    for post in feed.entries:
        if count % 5 == 1:
            title = feed['entries'][count].title
            url = feed['entries'][count].id
            bot.send_message( cid, str(title) +" " +str(url) ) 
        count += 1

@bot.message_handler(commands=['cuantarazon']) 
def command_cuantarazon(m): 
    feed = feedparser.parse('http://feeds.feedburner.com/cuantarazon')
    cid = m.chat.id
    # print all posts
    count = 1
    blockcount = 1
    for post in feed.entries:
        if count % 5 == 1:
            title = feed['entries'][count].title
            url = feed['entries'][count].id
            bot.send_message( cid, str(title) +" " +str(url) ) 
        count += 1
@bot.message_handler(commands=['dado']) 
def command_dado(m): 
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    dado = m.text[6:]
    if not dado:
        dado = 20
    dado = int(dado)
    numero = random.randrange(dado)
    bot.send_message( cid, "el Resultado del dado "+str(dado)+" es = "+str(numero) ) 


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if not str(cid) in usuarios: # Con esta sentencia, hacemos que solo se ejecute lo de abajo cuando un usuario hace uso del bot por primera vez.
        usuarios.append(str(cid)) # En caso de no estar en la lista de usuarios, lo añadimos.
        aux = open( 'usuarios.txt', 'a') # Y lo insertamos en el fichero 'usuarios.txt'
        aux.write( str(cid) + "\n")
        aux.close()
        bot.send_message( cid, "Bienvenido al bot!!!!")

@bot.message_handler(commands=['all'])
def command_all(m):
    cid = m.chat.id
    if cid != administrador: # Comprobamos que seamos nosotros quienes ejecutamos el comando
        bot.send_message( administrador, "El usuario con ID: " + str(cid) + " ha intentado utilizar el comando para enviar difundidos") # Si lo ejecuta otro, el bot nos avisará
    else: # Si somos nosotros...
        for ID in usuarios: # Por cada ID alamacenado en usuarios
            try: # Intentamos enviar el mensaje.
                bot.send_message( int(ID), m.text[4:])
            except: # Hacemos control de excepciones porque, si han borrado la conversación del bot o le han expulsado del grupo en el que estaba, se generará una excepción al intentar enviar el mensaje.
                bot.send_message( administrador, "Error enviando mensaje a: " + ID)
            else:
                bot.send_message( administrador, "Éxito enviando mensaje a: " + ID)



@bot.message_handler(commands=['tiempo'])
def command_tiempo(m):
    cid = m.chat.id
    token = m.text[7:]
    if (token == ""):
        token = "madrid"
    url = "https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\")&format=json&env=store://datatables.org/alltableswithkeys" % token
    
    try :
       link = urllib.urlopen(url)
       data = json.loads(link.read())
       tmp_min = (int(data['query']['results']['channel']['item']['forecast'][0]['high']) - 32) * 5.0/9.0
       tmp_max = (int(data['query']['results']['channel']['item']['forecast'][0]['low']) - 32) * 5.0/9.0
       custom_chain = """*Lugar*: """ + str(data['query']['results']['channel']['location']['city']) + """\n *Tiempo*: """ + str(data['query']['results']['channel']['item']['forecast'][0]['text']) + """\n *T.MIN*: """ + str(tmp_max) +  "º" + """\n *T.MAX* :""" + str(tmp_min) + "º" + """\n *Humedad*: """ + str(data['query']['results']['channel']['atmosphere']['humidity'] + "%")
       bot.send_message(cid, custom_chain, parse_mode="Markdown")
    except ValueError:
       bot.send_message( cid, 'No existe'+token)



@bot.message_handler(commands=['web']) 
def command_web(m): 
    cid = m.chat.id
    # 'Visita http://quiros.netai.net/'
    bot.send_message( cid,"pon tu web" ) 

@bot.message_handler(commands=["chuckjoke",])
def chuck_joke_handler(message):
    joke = pyjokes.get_joke(language='en', category='chuck')
    bot.send_message(message.chat.id, joke)
    
@bot.message_handler(commands=["joke",])
def joke_handler(message):
    joke = pyjokes.get_joke(language='en', category='all')
    bot.send_message(message.chat.id, joke)
    

@bot.message_handler(commands=["love",]) # Indicamos que lo siguiente va a controlar el comando '/miramacho'
def command_love(m): # Definimos una función que resuleva lo que necesitemos.
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    msg = m.text[6:]
    username = m.from_user.username
    if not msg:
        numero = random.randrange(7) 
        frases ={0:"Chris Hemsworth",
        1:"Joe Manganiello",
        2:"Elsa Pataky",
        3:"Charlize Theron",
        4:"Anna Simon",
        5:"Sofia Vergara",
        6:"Miguel Quiros",
        }
        msg = frases[numero]
    hdl = open('love.txt', 'r')
    milist = hdl.readlines()
    mensaje = random.choice(milist).replace("\n","")
    bot.send_message( cid, username +' '+ mensaje +' '+ msg ) # Con la función 'send_message()' del bot, enviamos al ID almacenado el texto que queremos.
    hdl.close()
    
    
@bot.message_handler(commands=['cena']) 
def command_cena(m): 
    cid = m.chat.id # Guardamos el ID de la conversación para poder responder.
    numero = random.randrange(7) 
    frases ={0:"Coger unas pizzas",
    1:"Cenar de raciones",
    2:"Gotardo",
    3:"Intentar entrar en el Oscar",
    4:"Podemos probar ir al Asturiano",
    5:"Chino de la calle villaverde",
    6:"Lavadero",
    }
    mensaje = frases[numero]
    bot.send_message( cid, mensaje)
    
@bot.message_handler(commands=['map'])
def command_map(m):
    cid = m.chat.id
    msg = m.text[5:]
    if not msg:
        bot.send_message(cid,"Esta funcion necesita una localizacion a buscar como argumento")
    else:
        toke = m.text.split(" ", 1)[1]
        toke = toke.encode('utf-8')
        url = "https://maps.googleapis.com/maps/api/staticmap?center=%s&zoom=14&size=400x400&maptype=hybrid&key=AIzaSyBmZVQKUXYXYVpY7l0b2fNso4z82H5tMvE" % toke
        urllib.urlretrieve(url, "map.png")
        bot.send_photo(cid, open( 'map.png', 'rb'))


@bot.message_handler(commands=['dia'])
def command_fecha(m):
    cid = m.chat.id
    x = datetime.datetime.now()
    switcher = {
        1: "enero",
        2: "febrero",
        3: "marzo",
        4: "abril",
        5: "mayo",
        6: "junio",
        7: "julio",
        8: "agosto",
        9: "septiembre",
        10: "octubre",
        11: "noviembre",
        12: "diciembre"
    }
    mes = switcher[x.month]
    fecha = "Hoy estamos a %s de %s" % (x.day, mes)
    bot.send_message(cid, fecha)
    bot.send_message(cid, "Y el tiempo de Madrid es:")
    token = "madrid"
    url = "https://query.yahooapis.com/v1/public/yql?q=select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"%s\")&format=json&env=store://datatables.org/alltableswithkeys" % token
    link = urllib.urlopen(url)
    data = json.loads(link.read())
    tmp_min = (int(data['query']['results']['channel']['item']['forecast'][0]['high']) - 32) * 5.0/9.0
    tmp_max = (int(data['query']['results']['channel']['item']['forecast'][0]['low']) - 32) * 5.0/9.0
    custom_chain = """*Lugar*: """ + str(data['query']['results']['channel']['location']['city']) + """\n *Tiempo*: """ + str(data['query']['results']['channel']['item']['forecast'][0]['text']) + """\n *T.MIN*: """ + str(tmp_max) +  "º" + """\n *T.MAX* :""" + str(tmp_min) + "º" + """\n *Humedad*: """ + str(data['query']['results']['channel']['atmosphere']['humidity'] + "%")
    bot.send_message(cid, custom_chain, parse_mode="Markdown")
    bot.send_message(cid, "Te voy a comentar que")
    command_frase(m)
       
        

@bot.message_handler(commands=['getid']) # sirve para averiguar tu id de forma basica 
def command_getid(m):
        cid = m.chat.id
        bot.send_message(cid, cid)

@bot.message_handler(commands=['creador'])
def command_iscreador(m):
        autorizado = 10721401
        cid = m.chat.id
    
        if(cid == autorizado):
            bot.send_message(cid, 'oh gran ineedblood mi creador')
        else:
            bot.send_message(cid, 'no eres mi craedor vete a la mierda')

@bot.message_handler(commands=['semanalmente'])
def command_semanal(m):
    cid = m.chat.id
    mensaje = "Viviremos con esto para siempre " # Poner aquí el mensaje a enviar
    while True:
        bot.send_message( cid, mensaje)
        time.sleep(segdia) 
        
@bot.message_handler(commands=['tetas','cerdas'])
def command_tits(m):
    cid = m.chat.id
    os.system("curl -Ls  \"http://www.hugeboobsbigtits.com/teen-big-tits\" | grep -o \'http[^\"]*.jpg\' > tits.txt")
    hdl = open('tits.txt', 'r')
    milist = hdl.readlines()
    line = random.choice(milist)
    bot.send_message( cid, line)
    hdl.close()

@bot.message_handler(commands=['tetazas'])
def command_bigtits(m):
    cid = m.chat.id
    os.system("curl -Ls  \"http://www.hugeboobsbigtits.com/big-natural-tits/\" | grep -o \'http[^\"]*.jpg\' > bigtits.txt")
    hdl = open('bigtits.txt', 'r')
    milist = hdl.readlines()
    line = random.choice(milist)
    bot.send_message( cid, line)
    hdl.close()


@bot.message_handler(commands=['chiste'])
def command_chiste(m):
    cid = m.chat.id
    test = m.chat
    print cid
    print test
    hdl = open('chistes.txt', 'r')
    milist = hdl.readlines()
    line = random.choice(milist)
    bot.send_message( cid, line)
    hdl.close()

@bot.message_handler(commands=['frase'])
def command_frase(m):
    cid = m.chat.id 
    hdl = open('frases.txt', 'r')
    milist = hdl.readlines()
    line = random.choice(milist)
    bot.send_message( cid, line)
    hdl.close()

@bot.message_handler(commands=['creavotacion'])
def command_votacion(m):
    cid = m.chat.id
    scid = str(cid)
    tema=m.text[14:]
    crea=open('votacion/votacion'+scid+'.txt','w')
    crea.close()
    crea=open('votacion/temario'+scid+'.txt','w')
    crea.write("tema de la votacion ="+tema)
    print tema
    command_voto(m)
    crea.close()

    

@bot.message_handler(commands=['leervotacion'])
def command_leervotacion(m):
    cid = m.chat.id
    scid = str(cid)
    archi=open('votacion/temario'+scid+'.txt','r')
    for linea in archi:
        milist=linea+"\n"
    archi.close() 
    archi=open('votacion/votacion'+scid+'.txt','r')
    for linea in archi:
        linea = re.sub('[^a-zA-Z0-9 \n\.]', ' ', linea)
        print linea
        milist=milist+linea
    archi.close() 
    print milist
    bot.send_message( cid, milist) 
    
@bot.message_handler(commands=['voto'])
def command_voto(m):   
    cid = m.chat.id
    scid = str(cid)
    archi=open('votacion/temario'+scid+'.txt','r')
    msg=archi.readline()
    archi.close() 
    textaco = "Ejercer el voto sobre "+msg
    json_keyboard = json.dumps({'keyboard': [["/AFAVOR"], ["/ENCONTRA"]], 
                            'one_time_keyboard': True, 
                            'resize_keyboard': True})
    bot.send_message( cid, textaco, reply_markup = json_keyboard)
    
#borrar custom keyboard
@bot.message_handler(commands=['remove'])
def command_remove(m):
    cid = m.chat.id
    json_keyboard = json.dumps({'hide_keyboard': True, 
                            'selective': False})
    bot.send_message(cid, "Voto Realizado" , reply_markup = json_keyboard)

@bot.message_handler(commands=['AFAVOR'])
def command_votook(m):   
    cid = m.chat.id
    scid = str(cid)
    if cid > 0:
        usuario = str(m.chat.first_name)
    else:
        usuario = str(m.from_user.first_name)
    existe=False
    f = open('votacion/votacion'+scid+'.txt','r')
    lines = f.readlines()
    for line in lines:
        
        palabras = line.split('·')
        for p in palabras:
            print p
            if p==usuario:
                existe=True
                bot.send_message( cid,usuario+" Ya has votado pesado")
    if not existe:  
        linea = usuario +"·OK"
        f = open('votacion/votacion'+scid+'.txt', 'a')
        f.write(linea + "\n") # Escribimos la linea de log en el fichero.
        f.close() # Cerramos el fichero para que se guarde.
        print "addvotook"+linea 
        command_remove(m)
    
    
@bot.message_handler(commands=['ENCONTRA'])
def command_votonok(m):   
    cid = m.chat.id
    scid = str(cid)
    if cid > 0:
        usuario = str(m.chat.first_name)
    else:
        usuario = str(m.from_user.first_name)
    existe=False
    f = open('votacion/votacion'+scid+'.txt','r')
    lines = f.readlines()
    for line in lines:
        palabras = line.split('·')
        for p in palabras:
            print p
            if p==usuario:
                existe=True
                bot.send_message( cid,usuario+" Ya has votado pesad@")
    if not existe:
        frase = usuario +"·NOK"
        f = open('votacion/votacion'+scid+'.txt', 'a')
        f.write(frase + "\n") # Escribimos la linea de log en el fichero.
        f.close() # Cerramos el fichero para que se guarde.
        print "addvotonok"+frase    
        command_remove(m)


@bot.message_handler(commands=['addfrase'])
def command_addfrase(m):
    cid = m.chat.id
    if cid > 0:
        frase = m.text[10:]
        if not frase:
            print "note hago caso"
        else:
            f = open('frases.txt', 'a')
            f.write(frase + "\n") # Escribimos la linea de log en el fichero.
            f.close() # Cerramos el fichero para que se guarde.
            print "addfrase "+frase
        
@bot.message_handler(commands=['addchiste'])
def command_addchiste(m):
    cid = m.chat.id
    if cid > 0:
        frase = m.text[10:]
        if not frase:
            print "note hago caso"
        else:
            f = open('chistes.txt', 'a')
            f.write(frase + "\n") # Escribimos la linea de log en el fichero.
            f.close() # Cerramos el fichero para que se guarde.
            print "addchiste "+frase
    
@bot.message_handler(commands=['addinsulto'])
def command_addinsulto(m):
    cid = m.chat.id
    if cid > 0:
        cid = m.chat.id
        frase = m.text[12:]
        if not frase:
            print "note hago caso"
        else:
            f = open('insultos.txt', 'a')
            f.write(frase + "\n") # Escribimos la linea de log en el fichero.
            f.close() # Cerramos el fichero para que se guarde.
            print "addinsulto "+frase
    

@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_text_insulto(m):
    cid = m.chat.id
    if cid > 0:
        usuario = str(m.chat.first_name)
    else:
        usuario = str(m.from_user.first_name)
    text = m.text
    texts = text.split(' ')
    dicho = False
    actuo = False
    for msg in texts:
        if not dicho:
            if (msg.lower() in ['pole']):
                bot.send_message(cid,usuario + '  ha hecho la pole')
                dicho = True
            elif (msg.lower() in ['puta','idiota','tonto','tonta','cabron']):  
                hdl = open('correctora.txt', 'r')
                milist = hdl.readlines()
                line = random.choice(milist)
                bot.send_message( cid, line)
                hdl.close()
                dicho = True
            elif (msg.lower() in ['voto']):  
                command_voto(m)
                dicho = True
            elif (msg in ['Tetas']):  
                command_tits(m)
                dicho = True
            elif (msg.lower() in ['cynthia','hola','@cynthiasbot','Cynthia','cyntia']):  
                hdl = open('saludos.txt', 'r')
                milist = hdl.readlines()
                line = random.choice(milist)
                bot.send_message( cid, line)
                hdl.close()
                dicho = True
            elif (msg.lower() in ['insulta']):
                print text
                print text.find("bot")
                if text.find("bot")>=0:
                        actuo = True
                elif text.find("Bot")>=0:
                        actuo = True
                elif text.find("BOT")>=0:
                        actuo = True
                else:
                    actuo = False
                print actuo
                if actuo:
                        hdl = open('insultos.txt', 'r')
                        milist = hdl.readlines()
                        line = random.choice(milist)
                        bot.send_message( cid,usuario+" me ha pedido que diga que : "+ line)
                        hdl.close()
                        dicho = True
    




#############################################


bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.