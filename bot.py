import os
import time
import json
import requests
import googletrans
from athus.modules import module
from athus.network import connect
from athus.commands import social
from athus.commands import music
from athus.commands import admin
from athus.commands import autoban
from athus.commands import translation
from athus.commands import api

class Athus(object):
	def __init__(self, name="zzz",icon="tanaka",room="EaUwgYdRqb"):
		self.name = name
		self.icon = icon
		self.file_name = 'athus/cache/athus.cookie'
		self.id = room

	def start(self):
		try:
			bot = connect.Connect(name=self.name, icon=self.icon)
			if not os.path.isfile(self.file_name):
				bot.login()
				bot.save_cookie(file_name=self.file_name)
			tradutor = translation.Translation(file_name=self.file_name)
			autobanimento = autoban.AutomaticBan(file_name=self.file_name)
			admn = admin.admininstrator(file_name=self.file_name,namebot=self.name)
			funny = social.Commands(file_name=self.file_name)
			musica = music.musicSistem(file_name=self.file_name)
			application = api.AthusWebsite()
			enter_room = module.Module(social=funny,
				                       music=musica,
				                       admin=admn,
				                       autoban=autobanimento,
				                       translation=tradutor,
				                       application=application)
			#sala para entrar
			url_room =f'https://drrr.com/room/?id={self.id}'
			enter_room.load_cookie(file_name=self.file_name)
			e_room = enter_room.room_enter(url_room=url_room)
			is_leave = enter_room.room_update()
		except Exception as e:
			print(e)

if __name__=='__main__':
	start = Athus()
	start.start()