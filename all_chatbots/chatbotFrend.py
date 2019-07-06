# coding: utf8

import random
import time
import json
from copy import copy
from chatbotFactBase import FactBase
from chatbotKnowlegeBase import KnowledgeBase


class ChatbotFrend(object):
    def __init__(self,knowledgeFile):
        self.variables = dict()
        self.state = "start"
        self.userResponse = "frendbot" # Chatbot response
        self.facts = FactBase() # Import FactBase from chatbot.py
        self.knowledgeBase = KnowledgeBase(knowledgeFile) # All our bot knowledge

    def chatWithAnotherChatbot(self):
        # response = "" # User response

        while self.state != "exit":
            # Debug
            print("state: ", self.state, " variables: ", self.variables, "\n")

            botQuestion = self.knowledgeBase.getQuestion(self.state,self.variables)
            print(botQuestion)
            print(self.state)
            print(self.userResponse)

            self.state = self.knowledgeBase.matchAnswer(self.state, self.variables, self.userResponse)
            self.userResponse = self.knowledgeBase.randomMatch(self.state)

            # gotoenum = []
            # variable,value,lowerResponse = self.knowledgeBase.find_facts_in_reponse(userResponse) # All the answers
            
            # # Enumerate all the state with description
            # for match,goto in self.knowledgeBase.enumerateAnswers(previousState):
            #     matchVariable = self.knowledgeBase.getVariable(match)
            #     if variable is None:
            #         if matchVariable is None:
            #             newMatch = userResponse
            #             description = match
            #         else:
            #             continue
            #     elif matchVariable is not None:
            #         if matchVariable.startswith(variable):
            #             newMatch = lowerResponse.replace(value,"@" + matchVariable) # replace the name value by the variable
            #             description = match.replace("@"+matchVariable,value.replace("_"," "))
            #         else:
            #             continue
            #     else:
            #         continue
            #     pos = len(gotoenum) + 1 
            #     gotoenum.append((newMatch,goto,matchVariable,value)) 
            
            #     print("%d) %s"%(pos,description))

            
            if self.state == "start":
                self.userResponse = "frendbot"
            elif self.state == "dont_understand":
                print("Sorry I don't understand '" + self.userResponse + "' I'm not very smart you know " )
                self.state = "what"

            time.sleep(5)
