# coding: utf8

import json
from copy import copy
from chatbotFactBase import FactBase
from chatbotKnowlegeBase import KnowledgeBase


class Scripted(object):
    def __init__(self,knowledgeFile):
        self.variables = dict()
        self.facts = FactBase() # Import FactBase from chatbot.py
        self.knowledgeBase = KnowledgeBase(knowledgeFile) # All our bot knowledge

    # chat instance loop
    def chat(self):
        self.state = "start"

        while self.state != "exit":
            # Debug
            print("state: ", self.state, " variables: ", self.variables)

            print("You can enter RESTART or BYE or EXIT at any moment\n")

            botQuestion = self.knowledgeBase.getQuestion(self.state,self.variables)
            userResponse = input(botQuestion + " ")
            self.state = self.knowledgeBase.matchAnswer(self.state, self.variables, userResponse)
            
            if self.state.startswith("exit"):
                self.state = "exit"
                break
            elif self.state == "dont_understand":
                print("Sorry I don't understand '" + userResponse + "' I'm not very smart you know " )
                self.state = "what"

