import string


import os
from PoS import PoS

class Predictor:    
    @staticmethod
    def predictMostFrequent(word) -> string:
        all_pos_path = os.path.join(os.getcwd(), 'all_pos.txt')
        with open(all_pos_path) as file:
            return PoS(file.readline().split(' / ')[0])
        
    @staticmethod
    def predictGlobalProbability(word) -> string:
        words_grouped = os.path.join(os.getcwd(), 'words_grouped.txt')
        pos_list=[]
        with open(words_grouped) as file:
            curr_word=None
            for line in file.readlines():
                if len(line.split(' / ')) == 1:
                    curr_word = line.strip()
                elif curr_word == word:
                    pos_list.append(PoS(line.split(' / ')[0], line.split(' / ')[1]))
        pos_list.sort(reverse=True)
        try:
            return pos_list[0]
        except:
            return PoS('not_found')
                