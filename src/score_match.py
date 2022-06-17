import os
import json
import numpy as np

prepositions = ['از', 'به', 'در', 'با']

'''
    This class provides functionalities to get weight of each word in scoring answers
    vocabDict is initiated each time server ran, if there is a vocab.json it is loaded, otherwise it is created
'''
class ScoreMatch:

    def __init__(self):
        self.vocabDict = {}
        if os.path.exists("vocabs.json"):
            with open('vocabs.json', 'r') as openfile:
                self.vocabDict = json.load(openfile)

    def score_vocab(self, vocab):
        if vocab not in self.vocabDict.keys():
            return 1
        return 1 / self.vocabDict[vocab]

    def store_sentence(self, sentence):
        vocabs = sentence.split(' ')
        for vocab in vocabs:
            if vocab not in prepositions:
                if vocab in self.vocabDict.keys():
                    self.vocabDict[vocab] += 1
                else:
                    self.vocabDict.update({vocab: 1})
        with open("vocabs.json", "w") as outfile:
            json.dump(self.vocabDict, outfile)
            outfile.close()

    ## score sentence based on vocabs
    ## ordering is not important
    def score_q(self, asked, saved_question):
        q1_vocabs = asked.split(" ")
        q2_vocabs = saved_question.split(" ")
        score = 0

        for vocab in q1_vocabs:
            if vocab in q2_vocabs:
                score += self.score_vocab(vocab)
        score /= len(saved_question.split(" "))
        return score