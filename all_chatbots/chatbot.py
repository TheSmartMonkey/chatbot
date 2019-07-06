# coding: utf8

import json
from copy import copy
from chatbotFactBase import FactBase
from chatbotKnowlegeBase import KnowledgeBase


class Chatbot(object):
    def __init__(self,knowledgeFile):
        self.variables = dict()
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
            previousState = self.state
            self.state = self.knowledgeBase.matchAnswer(self.state, self.variables, userResponse)

            if self.state == "dont_understand" and not userResponse.startswith("exit"):
                print("ok teach me something I love to learn, tell me what you means by : " + userResponse)
                gotoenum = []
                variable,value,lowerResponse = self.knowledgeBase.find_facts_in_reponse(userResponse) # All the answers
                
                # Enumerate all the state with description
                for match,goto in self.knowledgeBase.enumerateAnswers(previousState):
                    matchVariable = self.knowledgeBase.getVariable(match)
                    if variable is None:
                        if matchVariable is None:
                            newMatch = userResponse
                            description = match
                        else:
                            continue
                    elif matchVariable is not None:
                        if matchVariable.startswith(variable):
                            newMatch = lowerResponse.replace(value,"@" + matchVariable) # replace the name value by the variable
                            description = match.replace("@"+matchVariable,value.replace("_"," "))
                        else:
                            continue
                    else:
                        continue
                    pos = len(gotoenum) + 1 
                    gotoenum.append((newMatch,goto,matchVariable,value)) 
                
                    print("%d) %s"%(pos,description))


                while self.state != "exit":
                    choice = input("choose the good answer? ") # Let the user chose the good answer

                    # Go out of the chat
                    if choice.startswith("exit"):
                        self.state = "exit"
                        break

                    # Verify if user response is a integer
                    try:
                        option = int(choice)
                    except:
                        print("Not valid answer need an integer or BYE to quit")
                    
                    # Verify if the number correspond to an answer
                    if option > 0 and option < len(gotoenum) + 1:
                        match,goto,matchVariable,value = gotoenum[option-1]
                        self.knowledgeBase.addAnswer(previousState, match, goto)
                        if matchVariable is not None:
                            self.variables[matchVariable] = value
                        self.state = goto
                        break
                        
        self.knowledgeBase.dumpKnowledge() # Create or Update if exist a Json file
