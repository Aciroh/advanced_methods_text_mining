import os
import random
from typing import final
from Word import Word
from PoS import PoS
from Predictor import Predictor
from Evaluation import Evaluation

def read_files(train_percent):
  list_of_words = []
  directory = 'brown'
  cats_path = os.path.join(os.getcwd(), directory, 'cats.txt')
  list_of_files=[]
  with open(cats_path) as file:
    files = file.readlines()
    for file_name in files:
      list_of_files.append(file_name)
    random.shuffle(list_of_files)

    training_count = int((train_percent / 100) * len(list_of_files))
    result_count = len(list_of_files) - training_count


    training_files = list_of_files[:training_count]
    result_files = list_of_files[result_count:]
    for file_name in training_files:
      source_file_path = os.path.join(os.getcwd(), directory, file_name.split(' ')[0])
      with open(source_file_path) as source_file:

        word_lines = source_file.readlines()
        for word_line in word_lines:
          if any(char.isalpha() or char.isdigit() for char in word_line):

            for word_pos in word_line.split(' '):

              if len(word_pos.split('/'))==2:
                try:
                  word=Word(word_pos.split('/')[0],word_pos.split('/')[1])
                except:
                  continue
                else:
                  if word in list_of_words:

                    list_of_words[list_of_words.index(word)].inc()

                  else:
                    list_of_words.append(word)
                

  with open('Outputs/words_pos_count.txt', 'w') as f:
    f.write("Word / POS / COUNT\n")
    for word_pos in list_of_words:
        f.write("{} / {} / {}\n".format(word_pos.text,word_pos.pos, word_pos.count))
  return result_files

def read_output():
  words_pos_count_path = os.path.join(os.getcwd(), 'Outputs/words_pos_count.txt')
  words_list = []
  words_pos_list = []
  pos_list = []

  with open(words_pos_count_path) as file:
    lines = file.readlines()[1:]
    for word_pos in lines:
      try:
        word = Word(word_pos.split('/')[0],word_pos.split('/')[1],word_pos.split('/')[2])
      except:
        continue
      else: 
        words_pos_list.append(word)
        this_pos=PoS(word.pos)
        if this_pos not in pos_list:
          pos_list.append(this_pos)
        else:
          for pos in pos_list:
            if pos == this_pos:
              pos.inc()

        if word.text not in words_list:
          words_list.append(word.text)

  words_count = len(words_list)
  with open('Outputs/words_grouped.txt', 'w') as f:
    for word_text in words_list:
      f.write("\n{}\n".format(word_text))
      for word_pos in words_pos_list:
          if word_text == word_pos.text:
            f.write("{} / {}\n".format(word_pos.pos, word_pos.count))
  
  pos_list.sort(reverse=True)
  
  with open('Outputs/all_pos.txt', 'w') as f:
    for pos in pos_list:
      f.write("{} / {}\n".format(pos.pos,pos.count))
    f.write("words count / {}\n".format(words_count))

def predict(remaining_files):
  directory = 'brown'
  for file_name in remaining_files:
    source_file_path = os.path.join(os.getcwd(), directory, file_name.split(' ')[0])
    list_of_words = []
    list_of_pos = []
    list_of_evaluation=[]
    predictor = Predictor()
    with open(source_file_path) as source_file:
      word_lines = source_file.readlines()
      for word_line in word_lines:
        if any(char.isalpha() or char.isdigit() for char in word_line):
          for word_pos in word_line.split(' '):
            if len(word_pos.split('/'))==2:
              try:
                word=Word(word_pos.split('/')[0],word_pos.split('/')[1])
              except:
                continue
              else:
                pos = word.pos
                if pos not in list_of_pos:
                    list_of_pos.append(word.pos)
                if word not in list_of_words:
                  list_of_words.append(word)
      for item in list_of_pos:
        if item != 'None' and item is not None:
          list_of_evaluation.append(Evaluation(item))
      for word in list_of_words:
        print("\nPredictions for: {}".format(word.text))
        most_frequent_prediction = predictor.predictMostFrequent(word.text).pos
        print("Most Frequent: {}".format(most_frequent_prediction))
        for evaluation in list_of_evaluation:
          evaluation.checkEvaluation(most_frequent_prediction, word.pos)

      with open('Outputs/Predictions/most_frequent_results.txt', 'w') as f:
        for evaluation in list_of_evaluation:
          f.write("\n{}\nAccuracy: {}\nPrecision: {}\nRecall: {}\nSpecificity: {}\n".format(
            evaluation.pos,
            evaluation.getAccuracy(),
            evaluation.getPrecision(),
            evaluation.getRecall(),
            evaluation.getSpecificity()
            ))
      for evaluation in list_of_evaluation:
        evaluation.reset()
      for word in list_of_words:
        print("\nPredictions for: {}".format(word.text))
        global_probability_prediction = predictor.predictGlobalProbability(word.text).pos
        print("Most Frequent: {}".format(global_probability_prediction))
        for evaluation in list_of_evaluation:
          evaluation.checkEvaluation(global_probability_prediction, word.pos)
      with open('Outputs/Predictions/global_probability_results.txt', 'w') as f:
        for evaluation in list_of_evaluation:
          f.write("\n{}\nAccuracy: {}\nPrecision: {}\nRecall: {}\nSpecificity: {}\n".format(
            evaluation.pos,
            evaluation.getAccuracy(),
            evaluation.getPrecision(),
            evaluation.getRecall(),
            evaluation.getSpecificity()
            ))


        

if __name__=='__main__':
  remaining_files = read_files(70)
  read_output()
  print("Remaining number of files: {}".format(remaining_files))
  predict(remaining_files)
