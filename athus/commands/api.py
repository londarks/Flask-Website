import requests
import json

class AthusWebsite(object):
    def __init__(self):
        self.session = requests.session()

    def sendResquest(self,menssage, teste):
    	try:
	    	send = self.session.post(url="http://127.0.0.1/update/?menssage={}".format(menssage))
	    	send.close()
    	except Exception as e:
    		print(e)