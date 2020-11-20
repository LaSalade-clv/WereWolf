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
        logging.debug('# UPDATE')
        logging.debug(base_info)
        logging.debug(diff_data)

        #On mémorise les gens mort en baissant leurs score de haine
        if (request == 'DAILY_INITIALIZE'):
            for i in range(self.player_total):
                if (base_info['statusMap'][str(i+1)] == 'DEAD'):
                    self.player_score[i] -= 10000

        #On regarde dans diff_data pour les paroles / votes
        #logging.debug(diff_data)

        for row in diff_data.itertuples():
            type = getattr(row,'type')
            text = getattr(row,'text')
            if (type == 'vote'):
                voter = getattr(row,'idx')
                target = getattr(row,'agent')
                if target == self.myid:
                    #On est la cible du vote
                    logging.debug('Agent {} a voté pour moi !'.format(voter))
                    self.player_score[voter-1] += 100
            elif (type == 'talk' and '[{:02d}]'.format(self.myid) in text):
                #Ils ont parlé de moi
                source = getattr(row,'agent')
                logging.debug('Il a parle de moi : {}'.format(text))
                if 'WEREWOLF' in text or 'VOTE' in text:
                    #On se fait accusé de loupgarou
                    #On pense voter pour moi
                    self.player_score[source-1] += 10

                else:
                    #On a arreté de parlé de moi 
                    self.player_score[source-1] += 1
        self.hate = self.player_score.index(max(self.player_score)) + 1
        logging.debug('Hate Score: '+', '.join(str(x) for x in self.player_score))  

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
        logging.debug('# VOTE: '+str(self.hate))
        return self.hate
    
    def attack(self):
        logging.debug('# ATTACK: '+str(self.hate))
        return self.hate
    
    def divine(self):
        logging.debug('# DIVINE: '+str(self.hate))
        return self.hate
    
    def guard(self):
        logging.debug('# GUARD: '+str(self.hate))
        return self.hate
    
    def finish(self):
        return None
    


agent = SampleAgent(myname)
    


# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    