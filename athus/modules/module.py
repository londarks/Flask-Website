import requests
import time
import json
import re
import os
from random import randint 
import threading
import sys
import mimetypes
import datetime
import sqlite3



class Module(object):
    def __init__(self, social, music, admin, autoban, translation, application):
        self.session = requests.session()
        self.social = social
        self.music = music
        self.admin = admin
        self.flood = autoban
        self.api = application
        self.translation = translation
        self.usernameTrans = ''
        self.transBollean = False
        self.killProcess = False
        self.ban = True
        self.connection = sqlite3.connect('admin.db', check_same_thread=False)
        self.cursor = self.connection.cursor()
        #tripcode dos adms
        self.admin_list = ['ATHUSo12kM']#londarks tripcode

    def loadAdm(self, tripcode):
        with open('./Database/adm.json','r',encoding='utf-8') as json_file:
            admin = json.load(json_file)
            for i in range(len(admin)):
                if tripcode == admin[i]['Tripcode']:
                    return True
            return False

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url='https://drrr.com/room/?ajax=1', data=post_body)
        p.close()


    def martelo(self,idUser):
        ban_body = {
            'report_and_ban_user': idUser
        }
        kc = self.session.post('https://drrr.com/room/?ajax=1', ban_body)
        kc.close()

    def checkAdmin(self, tripcode):
        try:
            self.cursor.execute('SELECT tripcode From admin  WHERE tripcode="{}"'.format(tripcode))
            check = self.cursor.fetchall()
            return check[0][0]
        except Exception:
            return 'vazio'

    def load_cookie(self, file_name):
        f = open(file_name, 'r')
        self.session.cookies.update(eval(f.read()))
        f.close()

    def room_enter(self, url_room):
        re = self.session.get(url_room,headers={'User-Agent': 'Bot'})
        re.close()
        #room = self.session.get('https://drrr.com/json.php?fast=1')
        #return room.json()

    def returnIduser(self, idUser):
        try:
            rooms = self.session.get("https://drrr.com/json.php?update=")
            user = []
            if rooms.status_code == 200:
                rooms_data = json.loads(rooms.content)
            for rooms in rooms_data['users']:
                user.append(rooms)
            for j in range(len(user)):
                if user[j]['name'] == idUser:
                    try:
                        return user[j]['tripcode'],user[j]['id']
                    except Exception as e:
                        return "None",user[j]['id']
        except Exception:
            return "vazio"

    def checkBlackList(self, username, idUser, tripcode):
        #print(idUser)
        with open("Database/Database.json", "r",encoding='utf-8') as json_file:
            Blackusers = json.load(json_file)
        for i in range(len(Blackusers)):
            try:
                if tripcode == Blackusers[i]['Tripcode']:
                    self.martelo(idUser)
            except Exception as e:
                pass
        for a in range(len(Blackusers)):
            if username in Blackusers[a]['username']:
                self.martelo(idUser)

    def Blacklist(self, message, tripcode):
        try:
            if tripcode == self.admin_list[0]:
                user = message[8:]
                """ sistema de blacklist para imposibilitar a entrada de usuario que eu não quero na sala"""
                with open("Database/Database.json", "r") as file_object:
                    containts = json.load(file_object)
                #check user in the room
                itens = self.returnIduser(user)
                #insert user for json database
                insert = {"username" : user,"Tripcode" : itens[0]}
                containts.append(insert)

                with open("Database/Database.json", "w") as file_object:
                    json.dump(containts, file_object, indent=4)

                try:
                    self.martelo(itens[1])
                except Exception:
                    pass

        except Exception as e:
            print(e)

    def database(self,name,message):
        #time
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        data_atual = datetime.date.today()
        upTime = "{} | {}".format(current_time,data_atual)
        with open("athus/Database/log.json", "r",encoding='utf-8') as file_object:
            containts = json.load(file_object)
            insert = {"username" : name,"messagem" : message, "date": upTime}
            containts.append(insert)
        with open("athus/Database/log.json", "w",encoding='utf-8') as file_object:
            json.dump(accounts, file_object, ensure_ascii=False,indent=4)




    def room_update(self):
        t_loop = threading.Thread(target=self.admin.loop_msg)
        t_loop.start()
        #inicializando bot
        sendResponse  = self.session.get("https://drrr.com/json.php?fast=1")
        response = sendResponse.json()
        #condição para  ver se esta na sala ou não
        checkUpdate = response['update']
        while True:
            if self.killProcess == True:
                break
            #time.sleep(1)
            sendResponse  = self.session.get("https://drrr.com/json.php?fast=1")
            response = sendResponse.json()
            if checkUpdate != response['update']:
                try:
                    url_room_update = "https://drrr.com/json.php?update={}".format(response['update'])
                    msgApi = self.session.get(url_room_update).json()
                    #area da blacklist futuramente
                    #print("============================")
                    #print(msgApi)
                    #print("============================")
                    #verificando novos players == or black list
                    checkEnterRoom = msgApi['talks'][0]['type']
                    if checkEnterRoom == 'join':
                        name_sender = msgApi['talks'][0]['user']['name']
                        id_sender  = msgApi['talks'][0]['user']['id']
                        try:
                            tripcode = msgApi['talks'][0]['user']['tripcode']
                        except Exception:
                            tripcode = None
                        t_checkB = threading.Thread(target=self.checkBlackList, args=(name_sender,id_sender,tripcode))
                        t_checkB.start()  
                    #if checkEnterRoom == 'leave':
                        #if
                        #print(name_sender)
                        #print(id_sender)
                        #print(tripcode) 
                    # else:
                    #pegando dados dos usuarios que estao conversando
                    name_sender = msgApi['talks'][0]['from']['name']
                    id_sender  = msgApi['talks'][0]['from']['id']
                    #auto ban de floods
                    if name_sender != 'Athus':
                        self.flood.insetValue(name_sender)
                    try:
                        tripcode = msgApi['talks'][0]['from']['tripcode']
                    except Exception:
                        tripcode = None 
                    message = msgApi['talks'][0]['message']
                    #salvando dados
                    t_DB = threading.Thread(target=self.database, args=(name_sender,message))
                    t_DB.start()
                    #tradutor automatico
                    if self.transBollean == True:
                        if self.usernameTrans == name_sender:
                            self.translation.translationOnly(message,name_sender)
                    #fim do tradutor
                    #não se responde
                    if '/'  in message:
                        if name_sender == u'Athus':
                            continue
                        try:
                            checkPM = msgApi['talks'][0]['secret']
                            if checkPM == True:
                                name_sender = msgApi['talks'][0]['from']['name']
                                id_sender  = msgApi['talks'][0]['from']['id']
                                try:
                                    tripcode = msgApi['talks'][0]['from']['tripcode']
                                except Exception:
                                    tripcode = None
                                self.handle_private_message(message=message, id_sender=id_sender,
                                                                           name_sender=name_sender,tripcode=tripcode)
                        except Exception:
                            self.handle_message(message=message, name_sender=name_sender,
                                                            id_sender=id_sender,tripcode=tripcode)
                    #fim do loop
                    checkUpdate = response['update']
                except Exception as e:
                    pass



    def block (self, message, name_sender, tripcode, id_sender):
        message = message[7:]
        for i in range(len(self.admin_list)):
            if tripcode == self.admin_list[i]:
                if 'gif' in message:
                    t_gif = threading.Thread(
                        target=self.social.blockGifCommand)
                    t_gif.start()
                elif 'music' in message:
                    t_music = threading.Thread(
                        target=self.music.blockMusicCommand)
                    t_music.start()
                elif 'ship' in message:
                    t_ship = threading.Thread(
                        target=self.social.blockShipCommand)
                    t_ship.start()

    def anable (self, message, name_sender, tripcode, id_sender):
        message = message[8:]
        for i in range(len(self.admin_list)):
            if tripcode == self.admin_list[i]:
                if 'gif' in message:
                    t_gif = threading.Thread(
                        target=self.social.AnableGifCommand)
                    t_gif.start()
                elif 'music' in message:
                    t_music = threading.Thread(
                        target=self.music.AnableMusicCommand)
                    t_music.start()
                elif 'ship' in message:
                    t_ship = threading.Thread(
                        target=self.social.AnableShipCommand)
                    t_ship.start()

    def handle_message(self, message, name_sender, id_sender, tripcode):
        command = message
        if '/help' == command:
            t_help = threading.Thread(
                target=self.social.help, args=(message, name_sender))
            t_help.start()

        elif '/admin' == command:
            t_commandsAdmin = threading.Thread(
                target=self.admin.commandsAdmin)
            t_commandsAdmin.start()

        elif '/BL' == command:
            t_Blacklist = threading.Thread(target=self.admin.showBl)
            t_Blacklist.start()

        elif '/admin list' == command:
            t_listAdmin = threading.Thread(
                target=self.admin.adminList)
            t_listAdmin.start()

        elif '/play' == command:
            t_play = threading.Thread(
                target=self.music.thPlay)
            t_play.start()

        elif '/pause' == command:
            t_pause = threading.Thread(
                target=self.music.pause_playlist)
            t_pause.start()

        elif '/skip' == command:
            t_skip = threading.Thread(
                target=self.music.skip_playlist)
            t_skip.start()

        elif '/queue' == command:
            t_next = threading.Thread(
                target=self.music.next)
            t_next.start()

        elif '/list ban' == command:
            t_listban = threading.Thread(target=self.admin.listban)
            t_listban.start()

        elif '/clear list ban' == command:
            valid = self.loadAdm(tripcode)
            if valid == True:
                t_listban = threading.Thread(target=self.admin.clearlist)
                t_listban.start()

        elif '/help music' == command:
            t_music_help = threading.Thread(
                target=self.music.music_help, args=(message, name_sender))
            t_music_help.start()

        elif '/log' == command:
            t_music_help = threading.Thread(
                target=self.admin.log)
            t_music_help.start()

        elif '/stop_trans' == command:
            valid = self.loadAdm(tripcode)
            if valid == True:
                self.transBollean = False

        elif '/thanos' == message:
            t_thanos = threading.Thread(target=self.admin.thanos, args=(tripcode, name_sender))
            t_thanos.start()

        elif '/sera' in  message:
            t_sera = threading.Thread(
                target=self.social.ship, args=(message, name_sender))
            t_sera.start()

        elif '/report' in message:
            t_report = threading.Thread(target=self.Blacklist, args=(message, tripcode))
            t_report.start()

        elif '/trans' in message:
            valid = self.loadAdm(tripcode)
            if valid == True:
                #condições
                transMessage = re.findall(':.*', message)
                username= transMessage[0][2:]
                self.usernameTrans = username
                self.transBollean = True
                t_trans = threading.Thread(
                    target=self.translation.userTranslation, args=(message, name_sender))
                t_trans.start()

        elif '/gif' in message:
            t_ghipy = threading.Thread(
                target=self.social.ghipy, args=(message, name_sender, id_sender))
            t_ghipy.start()

        elif '/add' in message:
            t_music = threading.Thread(
                target=self.music.playlist, args=(message, name_sender, id_sender))
            t_music.start()


        elif '/t' in message:
            t_translation = threading.Thread(target=self.social.translation, args=(message, name_sender))
            t_translation.start()

#admin funçes
        elif '/set' in message:
            t_floodchat = threading.Thread(target=self.flood.floodchat, args=(message,tripcode))
            t_floodchat.start()

        elif '/kick' in message:
            t_adm_k = threading.Thread(target=self.admin.admin_kick, args=(message, name_sender, tripcode, id_sender))
            t_adm_k.start()

        elif '/ban' in message:
            t_ban = threading.Thread(target=self.admin.admin_ban, args=(message, name_sender, tripcode, id_sender))
            t_ban.start()

        elif '/unban' in message:
            t_ban = threading.Thread(target=self.admin.unbanOfficial, args=(message, tripcode))
            t_ban.start()

        elif '/block' in message:
            t_bloc = threading.Thread(target=self.block, args=(message, name_sender, tripcode, id_sender))
            t_bloc.start()

        elif '/enable' in message:
            t_anable = threading.Thread(target=self.anable, args=(message, name_sender, tripcode, id_sender))
            t_anable.start()

        elif'/room_name' in message:
            t_adm_name = threading.Thread(target=self.admin.setRomm_name, args=(message, tripcode))
            t_adm_name.start()

        elif'/room_info' in message:
            t_adm_description = threading.Thread(target=self.admin.setRomm_Description, args=(message, tripcode))
            t_adm_description.start()
#nivel londarks
        elif '/remove' in message:
            t_remove = threading.Thread(target=self.admin.removeAdm, args=(message,tripcode))
            t_remove.start()
        elif '/promote' in message:
            t_remove = threading.Thread(target=self.admin.addAdm, args=(message, tripcode))
            t_remove.start()


    def handle_private_message(self, message, id_sender, name_sender, tripcode):
        command = message
        if '/exit' == command:
            if tripcode == "ATHUSo12kM": #tripcode do dono do bot
                leave_body = {'leave': 'leave'}
                lr = self.session.post('https://drrr.com/room/?ajax=1', leave_body)
                lr.close()
                self.killProcess = True

        elif '/host' == command:
            self.admin.groom(new_host_id=id_sender, tripcode=tripcode)

        elif '/m_rebot' == command:
            t_skip = threading.Thread(target=self.music.rebotPlaylist)
            t_skip.start()

        elif '/troll_mode' == command:
            t_time = threading.Thread(target=self.autoban.troll)
            t_time.start()

        elif '/default_mode' == command:
            t_time = threading.Thread(target=self.autoban.defaultime)
            t_time.start()

        elif '/default' == command:
            t_default = threading.Thread(target=self.music.default)
            t_default.start()

        elif '/free' == command:
            t_free = threading.Thread(target=self.music.livre)
            t_free.start()

        elif '/say' in message:
            t_mensagemprivate = threading.Thread(target=self.social.mensagemprivate, args=(message, name_sender, id_sender))
            t_mensagemprivate.start()

        elif '/send' in command:
            t_sendMessage = threading.Thread(target=self.social.privatemenssagem, args=(message, name_sender))
            t_sendMessage.start()

        elif '/kick' in message:
            t_adm_k = threading.Thread(target=self.admin.admin_kick, args=(message, name_sender, tripcode, id_sender))
            t_adm_k.start()

        elif '/ban' in message:
            t_adm_ban = threading.Thread(target=self.admin.admin_ban, args=(message, name_sender, tripcode, id_sender))
            t_adm_ban.start()

        elif'/room_name' in message:
            t_adm_name = threading.Thread(target=self.admin.setRomm_name, args=(message, tripcode))
            t_adm_name.start()

        elif'/room_info' in message:
            t_adm_description = threading.Thread(target=self.admin.setRomm_Description, args=(message, tripcode))
            t_adm_description.start()

        elif '/remove' in message:
            t_remove = threading.Thread(target=self.admin.removeAdm, args=(message, tripcode))
            t_remove.start()
            #adiciona mais adm no sistema
        elif '/promote' in message:
            t_remove = threading.Thread(target=self.admin.addAdm, args=(message, tripcode))
            t_remove.start()
        return False