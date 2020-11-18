#!/usr/bin/env python
from __future__ import print_function, division 

from random import randint
import logging, json
# this is main script


import aiwolfpy
import aiwolfpy.contentbuilder as cb


'''
Alexis
L'agent agit en fonction des actions qui sont portées contre lui. 
'''


myname = 'renvenge{:02d}'.format(randint(0,99))

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

        #Initialise une liste avec un score de haine pour chaques joueur
        #On réduit son propre score afin de ne pas voter pour soit-même
        self.player_score = [0]*self.player_total
        self.player_score[self.myid-1] = -10000

        #On selectionne le joueur avec le plus de haine 
        self.hate = self.player_score.index(max(self.player_score)) + 1

    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        # print(base_info)
        # print(diff_data)
        
    def dayStart(self):
        return None
    
    def talk(self):
        return cb.over()
    
    def whisper(self):
        return cb.over()
        
    def vote(self):
        return self.base_info['agentIdx']
    
    def attack(self):
        return self.base_info['agentIdx']
    
    def divine(self):
        return self.base_info['agentIdx']
    
    def guard(self):
        return self.base_info['agentIdx']
    
    def finish(self):
        return None
    


agent = SampleAgent(myname)
    


# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    