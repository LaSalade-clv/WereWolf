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


myname = 'Liar{:02d}'.format(randint(0,99))

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

        # mémorise du faux rôle de l'agent
        self.myRole = 'SEER'
        logging.debug('# INIT : Je suis l\'agent ' + str(self.base_info['agentIdx']))

        # mémorisation des autres joueurs
        self.player_total = game_setting['playerNum']
        self.player_list = list(range(1, self.player_total+1))
        
        # Suppression de son entrée (pour ne pas se voter soi-même)
        self.player_list.remove(self.base_info['agentIdx'])

        # attribution d'un rôle aléatoire aux autres joueurs
        self.rolesDispo = ['VILLAGER', 'VILLAGER', 'VILLAGER', 'WEREWOLF', 'POSSESSED']
        self.player_fakeRole = ['UNKNOWN']*(self.player_total-1)
        self.attributionFakeRole()
        
        self.comingout = False
        self.wwNotReported = True

        self.deadRole = []

        self.target = 1
        self.fakeTargetDivine = 1

        # Sélection du faux loups-garous pour la divination
        self.fakeTargetDivine = self.player_fakeRole.index('WEREWOLF')+1

        

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


        if base_info['statusMap'][str(base_info['agentIdx'])] != 'DEAD':

            # On supprime les joueurs mort de la liste
            if (request == 'DAILY_INITIALIZE'):
                for i in self.player_list:
                    if (base_info['statusMap'][str(i)] == 'DEAD'):
                        j = self.player_list.index(i)
                        self.player_list.remove(i)
                        self.roleDead = self.player_fakeRole.pop(j)

                        if (i == self.fakeTargetDivine and self.base_info['myRole'] == 'WEREWOLF'):
                            self.rolesDispo.remove(self.roleDead)
                            
                        #elif (i == self.targetDivine and self.base_info['myRole'] == 'SEER'):


                
                # dans le cas où le rôle du bot est "Loups-Garous"
                if (base_info['myRole'] == 'WEREWOLF'):
                    
                    if ('WEREWOLF' in self.player_fakeRole) and (self.fakeTargetDivine == self.player_fakeRole.index('WEREWOLF')+1):
                        a=True
                    else:
                        # il n'y a plus de werewolf dans les fake rôles
                        # on réattribut les fake rôles
                        self.attributionFakeRole()
                        logging.debug(self.player_fakeRole)
                        logging.debug(self.rolesDispo)
                        # Sélection du faux loups-garous pour la divination
                        self.fakeTargetDivine = self.player_fakeRole.index('WEREWOLF')+1




                # dans le cas où le rôle du bot est "Voyante"
                if (base_info['myRole'] == 'SEER'):
                    if base_info:
                        for ligne in diff_data.values:
                            # on vérifie chaque entrée de divination
                            if (ligne[1] == 'divine'):
                                self.text = ligne[5]
                                if ('WEREWOLF' in ligne[5]):
                                    self.werewolfFound(ligne[4])
                                    self.roleTargetDivine = 'WEREWOLF'
                                else:
                                    self.targetDivine = ligne[4]
                                    self.roleTargetDivine = 'HUMAIN'
                                    self.player_list.remove(ligne[4])

            # On selectionne un joueur cible existant
            self.selectTarget()


    def dayStart(self):
        logging.debug('\n\n# DAYSTART')
        self.talk_turn = 0
        self.comingout = False
        self.wwNotReported = True
        return None
    

    def talk(self):
        logging.debug('\n# TALK')

        if self.base_info['myRole'] == 'VILLAGER' or self.base_info['myRole'] == 'POSSESSED':
            return 'ESTIMATE Agent[' + str(self.target) + '] WEREWOLF'

        self.talk_turn += 1

        #1 comingout
        if not self.comingout:

            # dans le cas où le rôle du bot est "WEREWOLF" ou "SEER"
            if  self.base_info['myRole'] == 'WEREWOLF' or self.base_info['myRole'] == 'SEER':
                self.comingout = True
                return cb.comingout(self.base_info['agentIdx'], self.myRole)

        #2 report
        if self.wwNotReported:
            self.wwNotReported = False
            if  self.base_info['myRole'] == 'WEREWOLF':
                return 'DIVINED Agent[' + str(self.fakeTargetDivine) + '] ' + self.player_fakeRole[self.fakeTargetDivine-1]
            elif self.base_info['myRole'] == 'SEER':
                return self.text
            else:
                return 'DIVINED Agent[' + str(self.target) + '] WEREWOLF'
        
        #3 declare my vote
        if self.talk_turn == 3:
            if  self.base_info['myRole'] == 'WEREWOLF':
                return 'VOTE Agent[' + str(self.fakeTargetDivine) + ']'
            elif self.base_info['myRole'] == 'SEER':
                return 'VOTE Agent[' + str(self.target) + ']'

        return cb.over()
    

    def whisper(self):
        logging.debug('\n# WHISPER')
        return cb.over()
        

    def vote(self):
        logging.debug('\n# VOTE: ')
        if  self.base_info['myRole'] == 'WEREWOLF':
            return self.fakeTargetDivine
        elif self.base_info['myRole'] == 'SEER':
            return self.target
        else:
            return self.target
    

    def attack(self):
        logging.debug('\n# ATTACK: ')
        return self.target
    

    def divine(self):
        logging.debug('\n# DIVINE: '+str(self.target))
        return self.target
    

    def guard(self):
        logging.debug('\n# GUARD: ')
        return self.base_info['agentIdx']
    

    def finish(self):
        return None


    def selectTarget(self):
        while self.randomNumber not in self.player_list:
            self.randomNumber = randint(1,self.player_total)
        self.target = self.randomNumber
    
    
    def werewolfFound(self, numero):
        liste = self.player_list.copy()
        for i in self.player_list:
            if (i != numero):
                liste.remove(i)
        self.targetDivine = numero
        self.target = numero
        self.player_list = liste
    
    
    def attributionFakeRole(self):
        role = self.rolesDispo.copy()
        i = 0
        while len(role) != 0 and i < len(self.player_fakeRole):
            r = randint(0,len(role)-1)
            if self.player_fakeRole[i] == 'UNKNOWN':
                self.player_fakeRole[i] = role.pop(r)
            i = i+1
    


agent = SampleAgent(myname)
    


# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    