import requests
import time
import json
import re
import os
import threading
import sys
import mimetypes
from googletrans import Translator


class Translation(object):
    def __init__(self, file_name):
        self.session = requests.session()
        self.host = 'https://drrr.com/room/?ajax=1'
        self.file = open(file_name, 'r')
        self.session.cookies.update(eval(self.file.read()))
        self.file.close()
        self.country = 'pt'

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url=self.host, data=post_body)
        p.close()



    def userTranslation (self, message, name_sender):
        try:
            lings = ["af","sq","am","ar","hy","az","eu","be","bn","bs","bg","ca","ceb","zh",
                 "zh-TW""co","hr","cs","da","nl","en","eo","et","fi","fr","fy","gl","ka",
                 "de","el","gu","ht","ha","haw""iw","hi","hmn","hu","is","ig","id","ga",
                 "it","ja","jv","kn","kk","km","rw","ko","ku","ky","lo","la","lv","lt",
                 "lb","mk","mg","ms","ml","mt","mi","mr","mn","my","ne","no","ny","or",
                 "ps","fa","pl","pt","pa","ro","ru","sm","gd","sr","st","sn","sd","si",
                 "sk","sl","so","es","su","sw","sv","tl","tg","ta","tt","te","th","tr",
                 "tk","uk","ur","ug","uz","vi","cy","xh","yi","yo","zu",]
            arg = re.findall('.*:', message)
            notfound = False
            text = arg[0][7:]
            remove = len(text)
            country = text[:remove - 1]
            for i in range(len(lings)):
                if country == lings[i]:
                    self.country = country
                    notfound = True
                    break
            if notfound == False:
                self.post(message='/me sigla invalida')
        except Exception:
            pass

    def translationOnly(self, message, name_sender):
        #======tradução=========#
        try:
            translator = Translator()
            traduzido=translator.translate(message, dest=self.country)
            self.post(message='[{}]:{}'.format(name_sender, traduzido.text))
        except Exception:
            pass