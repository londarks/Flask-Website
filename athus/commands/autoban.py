import requests
import time
import json
import re
import os
import threading
import sys
import mimetypes


class AutomaticBan(object):
    def __init__(self, file_name):
        self.session = requests.session()
        self.host = 'https://drrr.com/room/?ajax=1'
        self.file = open(file_name, 'r')
        self.flood = {}
        self.ban = 'ban'
        self.interuptor = True
        self.session.cookies.update(eval(self.file.read()))
        self.file.close()
        self.timeFlood = 8


    def troll(self):
    	self.timeFlood = 12
    	self.post(message="/me modo anti-troll ativado evitar mandar muitas menssagens")

    def defaultime(self):
    	self.timeFlood = 8


    def loadAdm(self, tripcode):
        with open('athus/Database/adm.json','r',encoding='utf-8') as json_file:
            admin = json.load(json_file)
            for i in range(len(admin)):
                if tripcode == admin[i]['Tripcode']:
                    return True
            return False

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

    def floodpunichs (self, iduser):
        ban_user = {
            self.ban : iduser
        }
        lr = self.session.post('https://drrr.com/room/?ajax=1', ban_user)
        lr.close()



    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url=self.host, data=post_body)
        p.close()


    def floodchat(self, message, tripcode):
        search = message [5:]
        valid = self.loadAdm(tripcode)
        try:
            if valid == True:
                if search == "none":
                    self.ban = 'ban'
                    self.post(message="/me Banimento por Cookie Ativado")
                elif search == "troll":
                    self.ban = 'report_and_ban_user'
                    self.post(message="/me Banimento por IP Ativado")
        except Exception as e:
            pass

#anti flood
    def insetValue(self, name):
        #ligando o clear de menssagens
        if self.interuptor == True:
            t_hiler = threading.Thread(target=self.limpalista)
            t_hiler.start()
            self.interuptor = False
        #regulando as menssagens
        if name in self.flood:
            self.flood[name] += 1
            if self.flood[name] > 5:
                iduser  = self.returnIduser(name)
                self.floodpunichs(iduser)
                self.post(message="/me {} Banido Por Flood".format(name))
        else:
            self.flood[name] = 1

    def limpalista(self):
        while True:
            time.sleep(self.timeFlood)
            self.flood = {}
