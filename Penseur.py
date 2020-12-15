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


myname = 'Suiveur{:02d}'.format(randint(0,99))

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

        self.player_suivi = [0]*self.player_total
        self.player_suivi[self.myid-1] = -10000

        #On selectionne le joueur avec le plus de haine 
        self.suspect = self.player_suspect.index(max(self.player_suspect)) + 1

    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        # print(base_info)
        # print(diff_data)
        logging.debug('# UPDATE jour : {}'.format(diff_data.getattr('day')))
        logging.debug(base_info)

        #On mémorise les gens mort en baissant leurs score de haine
        if (request == 'DAILY_INITIALIZE'):
            for i in range(self.player_total):
                if (base_info['statusMap'][str(i+1)] == 'DEAD'):
                    self.player_suspect[i] -= 10000
                    self.player_suivi[i] -= 10000


        #On regarde dans diff_data pour les paroles / votes
        logging.debug(diff_data)

        for row in diff_data.itertuples():
            type = getattr(row,'type')
            text = getattr(row,'text')

            #Lors du vote
            if (type == 'vote'):
                ...
         

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
        logging.debug(hatecycle[randint(0,2)].format(self.hate))
        return hatecycle[randint(0,2)].format(self.hate)
    
    def whisper(self):
        logging.debug('# WHISPER')
        return 'ATTACK Agent[{:02d}]'.format(self.hate)
        
    def vote(self):
        logging.debug('# VOTE: ')
        return self.hate
    
    def attack(self):
        logging.debug('# ATTACK: ')
        return self.hate
    
    def divine(self):
        logging.debug('# DIVINE: ')
        return self.hate
    
    def guard(self):
        logging.debug('# GUARD: ')
        return self.hate
    
    def finish(self):
        return None
    

agent = SampleAgent(myname)

# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    