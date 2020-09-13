import requests
import time
import json
import re
import os
from random import randint
import threading
import sys
import mimetypes
from googletrans import Translator


class Commands(object):
    def __init__(self, file_name):
        self.session = requests.session()
        self.host = 'https://drrr.com/room/?ajax=1'
        self.spam = {"gif": False, "help": False, "ship":False,"rules":False,"trans":False}
        self.file = open(file_name, 'r')
        self.blockship = True
        self.blockgif = True
        self.session.cookies.update(eval(self.file.read()))
        self.file.close()

    def returnIduser(self, idUser):
        rooms = self.session.get("https://drrr.com/json.php?update=")
        user = []
        if rooms.status_code == 200:
            rooms_data = json.loads(rooms.content)
        for rooms in rooms_data['users']:
            user.append(rooms)
        for j in range(len(user)):
            if user[j]['name'] == idUser:
                return user[j]['id']

    def blockShipCommand(self):
        self.blockship = False

    def AnableShipCommand(self):
        self.blockship = True

    def blockGifCommand(self):
        self.blockgif = False

    def AnableGifCommand(self):
        self.blockgif = True

    def avoid_spam(self, com):
        time.sleep(5)
        self.spam[com] = False

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url=self.host, data=post_body)
        p.close()

    def mensagemprivate(self, message, name_sender, to=''):
        if re.findall('/say .*', message):
           message = message[5:] #conta 5 carateres e depois imprime aquilo escrito
           self.post(message='%s' % (message)) #imprime a menssagem dita

    def help(self, message, name_sender):
        commandName = 'help'
        if self.spam[commandName] == False:
            try:
                self.post(
                    message="Comandos:\n|/help music|\n|/gif|\n|/add|\n|/queue|\n|/pause|\n|/play|\n|/skip|\n|/ship|\n|/t|")
                self.spam[commandName] = True
                self.avoid_spam(commandName)
            except Exception as e:
                pass

    def ghipy(self, message, name_sender, id_sender):
        commandName = 'gif'
        if self.spam[commandName] == False:
            if self.blockgif == True:
                message = message[5:]

                apikey = "LIVDSRZULELA"  # test value
                lmt = 8
                list_gif = []
                # our test search
                search_term = message

                r = requests.get(
                    "https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, lmt))
                if r.status_code == 200:
                    top_8gifs = json.loads(r.content)
                    maximo = len(top_8gifs['results']) - 1
                    x = randint(0, maximo)
                    list_gif.append(top_8gifs['results'][x])
                    url = list_gif[0]['media'][0]['mediumgif']['url']
                self.post(message='{}-@{}'.format(message, name_sender),
                          url='%s' % (url))
            else:
                self.post(message='/me Comando Bloqueado')
            self.spam[commandName] = True
            self.avoid_spam(commandName)


    def ship(self, message, name_sender):
        commandName = 'ship'
        if self.spam[commandName] == False:
            if self.blockship == True:
                message = message[5:]
                x = randint(0, 10)
                ship = ""
                switcher = {
                   0: "0%",
                   1: "10%",
                   2: "20%",
                   3: "30%",
                   4: "40%",
                   5: "50%",
                   6: "60%",
                   7: "70%",
                   8: "80%",
                   9: "90%",
                   10:"100%"
                }
                for i in range(0,x):
                    ship += "█"
                total = switcher.get(x)
                self.post(message='A chance de:\n"{}"\nSão:\n{}{}'.format(message,ship,total))
            else:
                self.post(message='/me Comando Bloqueado')
            self.spam[commandName] = True
            self.avoid_spam(commandName)

    def translation (self, message, name_sender):
        commandName = 'trans'
        lings = ["af","sq","am","ar","hy","az","eu","be","bn","bs","bg","ca","ceb","zh",
                 "zh-TW""co","hr","cs","da","nl","en","eo","et","fi","fr","fy","gl","ka",
                 "de","el","gu","ht","ha","haw""iw","hi","hmn","hu","is","ig","id","ga",
                 "it","ja","jv","kn","kk","km","rw","ko","ku","ky","lo","la","lv","lt",
                 "lb","mk","mg","ms","ml","mt","mi","mr","mn","my","ne","no","ny","or",
                 "ps","fa","pl","pt","pa","ro","ru","sm","gd","sr","st","sn","sd","si",
                 "sk","sl","so","es","su","sw","sv","tl","tg","ta","tt","te","th","tr",
                 "tk","uk","ur","ug","uz","vi","cy","xh","yi","yo","zu",]
        if self.spam[commandName] == False:
            self.spam[commandName] = True
            try:
                notSend = False
                arg = re.findall('.*:', message)
                transMessage = re.findall(':.*', message)
                text = arg[0][3:]
                remove = len(text)
                country = text[:remove - 1]
                transM= transMessage[0][1:]
                #======tradução=========#
                for i in range(len(lings)):
                    if country == lings[i]:
                        translator = Translator()
                        traduzido=translator.translate(transM, dest=country)
                        self.post(message='{}'.format(traduzido.text))
                        self.avoid_spam(commandName)
                        notSend = True
                        break
                if notSend == False:
                    self.post(message='/me sigla invalida')
                    self.avoid_spam(commandName)
            except Exception:
                self.avoid_spam(commandName)


    def privatemenssagem (self, message, name_sender):
        try:
            toMessage = re.findall('.*:', message)
            sendMessage = re.findall(':.*', message)
            sendD = toMessage[0][6:]
            sendM= sendMessage[0][1:]
            remove = len(sendD)
            avalid = sendD[:remove-1]
            usuario = self.returnIduser(avalid)
            self.post(message=sendM, to=usuario)
        except Exception:
            pass