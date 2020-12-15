#!/usr/bin/env python
from __future__ import print_function, division 

from random import randint
import logging, json
# this is main script


import aiwolfpy
import aiwolfpy.contentbuilder as cb


'''
Antoine
L'agent agit de façon aléatoire.  Si l'agent est voyante, alors il peut éliminer les personnes villageoises de la liste des suspects.
'''


myname = 'ALittleBitRandom{:02d}'.format(randint(0,99))

class SampleAgent(object):
    
    def __init__(self, agent_name):
        # myname
        self.myname = agent_name
        logging.basicConfig(filename=self.myname+'.log',
                            level=logging.DEBUG,
                            format='')
        
        
    def getName(self):
        return self.myname
    

    def initialize(self, base_info, diff_data, game_setting):
        self.base_info = base_info
        # game_setting
        self.game_setting = game_setting
        
        #print(base_info)
        #print(diff_data)
        #print(game_setting)

        # mémorise l'id de l'agent
        self.myid = base_info['agentIdx']
        logging.debug('# INIT : Je suis l\'agent ' + str(self.myid))

        # Mémorisation des autres joueurs
        self.player_total = game_setting['playerNum']
        self.player_list = list(range(1, self.player_total+1))

        # Suppression de son entrée (pour ne pas se voter soi-même)
        self.player_list.remove(self.myid)

        # Sélection d'un nombre aléatoire
        self.randomNumber = randint(1,self.player_total)

        # On selectionne un joueur cible existant
        while self.randomNumber not in self.player_list:
            self.randomNumber = randint(1,self.player_total)
        self.target = self.randomNumber


    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        # print(base_info)
        # print(diff_data)
        logging.debug('\n### UPDATE')
        logging.debug(request)
        logging.debug('### ' + str(base_info))
        logging.debug('### ' + str(diff_data))

        # On supprime les joueurs mort de la liste
        if (request == 'DAILY_INITIALIZE'):
            for i in self.player_list:
                if (base_info['statusMap'][str(i)] == 'DEAD'):
                    self.player_list.remove(i)

            # dans le cas où le rôle du bot est "Voyante"
            if (base_info['myRole'] == 'SEER'):
                if base_info:
                    for ligne in diff_data.values:
                        # on vérifie chaque entrée de divination
                        if (ligne[1] == 'divine'):
                            if ('WEREWOLF' in ligne[5]):
                                self.werewolfFound(ligne[4])
                            elif (ligne[4] in self.player_list):
                                self.player_list.remove(ligne[4])


        # On selectionne un joueur cible existant
        self.selectRandom()

        logging.debug('\n### Je vote aléatoirement pour ' + str(self.target))
        logging.debug('Liste des joueurs restants : ' + ', '.join(str(x) for x in self.player_list))


    def dayStart(self):
        logging.debug('\n\n# DAYSTART')
        return None
    
    def talk(self):
        logging.debug('\n# TALK')
        logging.debug('ESTIMATE Agent[{:02d}] WEREWOLF'.format(self.target))
        return 'ESTIMATE Agent[{:02d}] WEREWOLF'.format(self.target)
    
    def whisper(self):
        logging.debug('\n# WHISPER')
        return 'ATTACK Agent[{:02d}]'.format(self.target)
        
    def vote(self):
        logging.debug('\n# VOTE: '+str(self.target))
        return self.target
    
    def attack(self):
        logging.debug('\n# ATTACK: '+str(self.target))
        return self.target
    
    def divine(self):
        logging.debug('\n# DIVINE: '+str(self.target))
        return self.target
    
    def guard(self):
        logging.debug('\n# GUARD: '+str(self.target))
        return self.target
    
    def finish(self):
        return None


    def selectRandom(self):
        while self.randomNumber not in self.player_list:
            self.randomNumber = randint(1,self.player_total)
        self.target = self.randomNumber
    
    
    def werewolfFound(self, numero):
        for i in self.player_list:
            if (i != numero):
                self.player_list.remove(i)
        self.target = numero
    


agent = SampleAgent(myname)
    


# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    