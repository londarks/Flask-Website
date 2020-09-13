import requests
import time
import json
import re
import os
from random import randint
import threading
import sys
import mimetypes


class RealPersonGame(object):
    def __init__(self, file_name):
        self.session = requests.session()
        self.host = 'https://drrr.com/room/?ajax=1'
        self.file = open(file_name, 'r')
        self.session.cookies.update(eval(self.file.read()))
        self.file.close()
        #rpg
        self.blockjoin = False
        self.name_joinGame = []
        self.id_joinGame = []
        self.name_killer = ""
        self.id_killer = ""
        self.morto = ""
        self.kill = False
        self.vote = []


    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url=self.host, data=post_body)
        p.close()

    def matadoro(self, killplayer, id_sender):
        death = killplayer[6:]
        if self.id_killer == id_sender:
            self.post(message='você matou: {}'.format(death), to=id_sender)
            self.morto = death
            print("morto: {} , Matador: {}".format(self.morto, self.name_killer))

    def lixamento(self, message, id_sender):
    	for a in range(len(self.id_joinGame)):
    		if id_sender == self.id_joinGame[a]:
    			vote = message[6:]
    			self.vote.append(vote)

    def removeList(self, persson):
        sobreviventes = ""
        for r in range(len(self.name_joinGame)-1):
        	if persson in self.name_joinGame[r]:
        		print("retirado: {}, id_removido: {}".format(self.name_joinGame[r], self.id_joinGame[r]))
        		self.name_joinGame.remove(self.name_joinGame[r])
        		self.id_joinGame.remove(self.id_joinGame[r])
        #mostrando sobreviventes
        for z in range(len(self.name_joinGame)):
        	sobreviventes += "|{}|\n".format(self.name_joinGame[z])
        self.post(message='sobreviventes:\n{}'.format(sobreviventes))
        #=======================================

    def startgame(self):
        if len(self.name_joinGame) >1:
            rodada = 1
            self.post(message='/me rodada {}'.format(rodada))
            sobreviventes = ""
            self.blockjoin = False
            sortKiller = randint(0, len(self.name_joinGame)-1)
            killer = self.name_joinGame[sortKiller]
            self.id_killer = self.id_joinGame[sortKiller]
            self.name_killer = self.name_joinGame[sortKiller]
            #manda pm pro assasino
            for i in range(len(self.name_joinGame)):
                time.sleep(4)
                if self.id_killer == self.id_joinGame[i]:
                    self.post(message='Você e o assasino: Digite /kill e o nome do player que voce quer matar quando eu disser: Cidade dorme', to=self.id_killer)
                    self.post(message='Digite: /vote player_name para se enturmar', to=self.id_joinGame[i])
                else:
                    self.post(message=' Você é um aldeão, Digite: /vote player_name para expulsar', to=self.id_joinGame[i])
            while True:
                rodada += 1
                self.post(message='/me Cidade Dorme')
                time.sleep(30)
                #caso assasino nao mate jogo acaba
                if self.morto == "":
                    self.post(message='/me Assasino Offline, jogo Acabou.!')
                    break
                self.post(message='/me {} Morreu.!'.format(self.morto))
                self.morto = ""
                #removendo morto
                self.removeList(self.morto)
                #=======================================
                self.post(message='sobreviventes:\n{}'.format(sobreviventes))
                self.post(message='/me cidade Acorda, Votem no Culpado')
                #time.sleep(60)
                self.post(message='/me Falta 2m para fechar a votação')
                time.sleep(60)
                #self.post(message='/me Falta 1m para fechar a votação')
                #time.sleep(60)
                sortelixamento = randint(0, len(self.vote)-1)
                self.post(message='/me vocês mataram {}.!'.format(self.vote[sortelixamento]))
                if self.vote[sortelixamento] in self.name_killer:
                    self.post(message='/me Assasino foi multilado! Fim de Jogo')
                    break
                self.removeList(self.vote[sortelixamento])
                self.vote = []
                self.post(message='/me rodada:{}'.format(rodada))
                if len(self.name_joinGame) == 1:
                    self.post(message='O assasino: {}, Ganhou o jogo'.format(self.name_killer))
                    break    
        
        else:
            self.post(message='/me Falta Jogadores.!')

    def start(self):
        self.post(message='/me digite /join para entrar no jogo')
        self.blockjoin = True
        #loop com tempo de 3 minutos 120 2m /180 3m
        #self.startgame()

    def insetusers(self, name_sender, id_sender):
        valid = True
        if self.blockjoin == True:
            players = "participantes\n"
            for a in range(len(self.name_joinGame)):
                if name_sender == self.name_joinGame[a]:
                    valid = False
            if valid == True:
                self.name_joinGame.append(name_sender)
                self.id_joinGame.append(id_sender)
                for i in range(len(self.name_joinGame)):
                    players += '|{}|\n'.format(self.name_joinGame[i])
                self.post(message="{}".format(players))
