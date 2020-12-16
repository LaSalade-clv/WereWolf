#!/usr/bin/env python
from __future__ import print_function, division 

from random import randint
import logging, json
# this is main script


import aiwolfpy
import aiwolfpy.contentbuilder as cb


'''
Alexis 
'''


myname = 'Penseur{:02d}'.format(randint(0,99))

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
        
        print(base_info)
        #print(diff_data)
        print('\n',game_setting)

        #mémorise l'id de l'agent
        self.myid = base_info['agentIdx']
        logging.debug('# INIT : I\'am agent {}'.format(self.myid))
        self.player_total = game_setting['playerNum']


        self.player_suspect = [0]*self.player_total
        self.player_suspect[self.myid-1] = -10000


        self.historique_vote = [0]*self.player_total

        #On selectionne le joueur avec le plus de haine 
        self.suspect = self.player_suspect.index(max(self.player_suspect)) + 1

    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        # print(base_info)
        # print(diff_data)
        logging.debug('# UPDATE jour : {}'.format('x'))
        #logging.debug(base_info)

        #On mémorise les gens mort en baissant leurs score de haine
        if (request == 'DAILY_INITIALIZE'):
            for i in range(self.player_total):
                if (base_info['statusMap'][str(i+1)] == 'DEAD'):
                    self.player_suspect[i] -= 10000

        if (base_info['myRole'] == 'SEER'):
            for ligne in diff_data.values:
             # on vérifie chaque entrée de divination
                if (ligne[1] == 'divine'):
                    if ('WEREWOLF' in ligne[5]):
                        self.player_suspect[ligne[4]-1] += 10000
                    else:
                        self.player_suspect[ligne[4]-1] -= 10000


        #On regarde dans diff_data pour les paroles / votes
        logging.debug(diff_data)

        for row in diff_data.itertuples():
            type = getattr(row,'type')

            #Lors du vote
            if (type == 'vote'):
                voter = getattr(row,'idx')
                target = getattr(row,'agent')
                if getattr(row,'day') >= 2:
                    x=0
                    logging.debug('voter/target{}:'.format(x))
                    x+=1
                    logging.debug(voter)
                    logging.debug(target)
                    if self.historique_vote[voter-1] == target:
                        self.player_suspect[target-1] += 1000
               

                self.historique_vote[voter-1] = target

        logging.debug('suspect:')
        logging.debug(self.historique_vote)

        logging.debug(self.player_suspect)



         

    def dayStart(self):
        logging.debug('# DAYSTART')
        return None
    
    def talk(self):
        logging.debug('# TALK')

        hatecycle =[
            'REQUEST ANY (VOTE Agent[{:02d}])',
            'ESTIMATE Agent[{:02d}] WEREWOLF',
            'VOTE Agent [{:02d}]',
        ]
        logging.debug(hatecycle[randint(0,2)].format(self.suspect))
        return hatecycle[randint(0,2)].format(self.suspect)
    
    def whisper(self):
        logging.debug('# WHISPER')
        return 'ATTACK Agent[{:02d}]'.format(self.suspect)
        
    def vote(self):
        logging.debug('# VOTE: ')
        return self.suspect
    
    def attack(self):
        logging.debug('# ATTACK: ')
        return self.suspect
    
    def divine(self):
        logging.debug('# DIVINE: ')
        return self.suspect
    
    def guard(self):
        logging.debug('# GUARD: ')
        return self.suspect
    
    def finish(self):
        return None
    

agent = SampleAgent(myname)

# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    