import time
import json
import base64
import requests
import datetime

class WebsiteControl(object):
	"""docstring for WebsiteControl"""
	def __init__(self, ):
		self.users = 0
		self.session = requests.session()
		self.host = 'https://drrr.com/room/?ajax=1'
		self.file = open('athus/cache/athus.cookie', 'r')
		self.session.cookies.update(eval(self.file.read()))
		self.start_time = datetime.datetime.utcnow()


	def post(self, message, url='', to=''):
		post_body = {
			'message': message,
			'url': url,
			'to': to
			}
		p = self.session.post(
			url=self.host, data=post_body)
		p.close()

	def share_music(self, url, name=''):
		share_music_body = {
			'music': 'music',
			'name': name,
			'url': url}
		p = self.session.post(url=self.host, data=share_music_body)
		p.close()

	def timeOnline(self):
		now = datetime.datetime.utcnow() # Timestamp of when uptime function is run
		delta = now - self.start_time
		hours, remainder = divmod(int(delta.total_seconds()), 3600)
		minutes, seconds = divmod(remainder, 60)
		days, hours = divmod(hours, 24)
		if days:
			time_format = "{d}D-{h}H:{m}M:{s}S"
		else:
			time_format = "{d}D-{h}H:{m}M:{s}S"
		uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
		print(uptime_stamp)
		return uptime_stamp

	def deleteBlacklis(self,username):
		with open("athus/Database/Database.json", "r", encoding='utf-8') as file_object:
			accounts = json.load(file_object)

		for i in range(len(accounts)):
			if accounts[i]["username"] == username:
				accounts.pop(i)
				break
		with open("athus/Database/Database.json", "w", encoding="utf-8") as file_object:
			json.dump(accounts, file_object, ensure_ascii=False,indent=4)

	def insetBlacklist(self, iduser):
		online  = self.Dashboard()
		data_atual = datetime.date.today()
		for i in range(len(online)):
			if online[i]['id'] == iduser:
				with open("athus/Database/Database.json", "r", encoding='utf-8') as file_object:
					accounts = json.load(file_object)
					#tratando erro
					try:
						tripcode = online[i]['tripcode']
					except Exception:
						tripcode = ""
					#inserindo usuario
					insert = {"username" : online[i]['name'],"date" : "{}".format(data_atual),"Tripcode": tripcode}
					accounts.append(insert)
				#colocando usuario na black list
				with open("athus/Database/Database.json", "w", encoding="utf-8") as file_object:
					json.dump(accounts, file_object, ensure_ascii=False,indent=4)
    

	def kick(self,name,adm):
		kick_body = {
		'kick': name
		}
		kc = self.session.post('https://drrr.com/room/?ajax=1', kick_body)
		kc.close()

		base64_bytes = adm.encode('ascii')
		message_bytes = base64.b64decode(base64_bytes)
		adminstrator = message_bytes.decode('ascii')

		self.post(message="/me Usuario Kikado por: {}".format(adminstrator))

	def ban(self,name,adm):
		ban_body = {
		'ban': name
		}
		kc = self.session.post('https://drrr.com/room/?ajax=1', ban_body)
		kc.close()

		base64_bytes = adm.encode('ascii')
		message_bytes = base64.b64decode(base64_bytes)
		adminstrator = message_bytes.decode('ascii')

		self.post(message="/me Usuario banido por: {}".format(adminstrator))

	def Dashboard(self):
		active = True
		usuarios = []
		tripcode = ""
		rooms = self.session.get("https://drrr.com/json.php?update=")
		user = []
		with open("athus/Database/adm.json", "r", encoding='utf-8') as file_object:
			admin = json.load(file_object)
		if rooms.status_code == 200:
			rooms_data = json.loads(rooms.content)
		for rooms in rooms_data['users']:
			user.append(rooms)
			self.users = len(user)
		for x in range(len(user)):
			for r in range(len(admin)):
				try:
					if user[x]['tripcode'] == admin[r]['Tripcode']:
						insert = {"name" : user[x]['name'],"tripcode" :user[x]['tripcode'] ,"acess": "ADM"}
						usuarios.append(insert)
						active = False
						break
					else:
						tripcode = user[x]['tripcode']
						active = True
				except Exception:
					tripcode = ""
			if active:
				insert = {"name" : user[x]['name'],"tripcode" : tripcode ,"acess": "user"}
				usuarios.append(insert)
				active = True
		return usuarios

	def reload(self): 
		return self.users

	def checkLogin(self, username, password):
		with open('Database/database.json','r',encoding='utf-8') as json_file:
			accounts = json.load(json_file)
		for i in range(len(accounts)):
			if username == accounts[i]['username']:
				if accounts[i]['password'] == password:
					oauthname = accounts[i]['username'].encode('ascii')
					#criptografando
					base64_user = base64.b64encode(oauthname)
					#mandando
					oauthname = base64_user.decode('ascii')
					acess = str(accounts[i]['acess'])
					return oauthname,acess
		return "invalid"

	def register(self,username,password):
		with open("Database/database.json", "r") as file_object:
			containts = json.load(file_object)
			insert = {"username" : username,"password" : password,"acess": "1w38D)rs"}
			containts.append(insert)

		with open("Database/database.json", "w") as file_object:
			json.dump(containts, file_object, indent=4)

	def blacklist(self):
		with open("athus/Database/Database.json", "r", encoding='utf-8') as file_object:
			accounts = json.load(file_object)
			return accounts

	def adminstrator(self):
		with open("athus/Database/adm.json", "r", encoding='utf-8') as file_object:
			admin = json.load(file_object)
			return admin

	def adminOnline(self):
		adm_online = 0
		with open("athus/Database/adm.json", "r", encoding='utf-8') as file_object:
			admin = json.load(file_object)
		online  = self.Dashboard()
		for i in range(len(online)):
			for a in range(len(admin)):
				try:
					if online[i]['tripcode'] == admin[a]['Tripcode']:
						adm_online += 1
				except Exception :
					pass
		return adm_online

	def music(self):
		with open("athus/Database/music.json", "r", encoding='utf-8') as file_object:
			music = json.load(file_object)
		return music

	def play(self,link):
		self.share_music(url=link, name="song from website")

