# coding: utf8

import random
import string
import json
from copy import copy
from chatbotFactBase import FactBase


class KnowledgeBase(object):
        def __init__(self,knowledgeFile):
            self.states = json.load(open(knowledgeFile)) # All our bot knowledge
            self.facts = FactBase()

        def getQuestion(self,state,variables):
            """
            Retreve the questions for a current state
            """
            question = copy(self.states[state]["say"])

            # Remove the @ in the question 
            for var in variables:
                if "@" + var in question and variables[var] is not None:
                    question = question.replace("@"+var,variables[var])

            return question
        
        def getVariable(self,match):
            """
            Get the question variable in the knowledge base
            """
            listVariables = [tok[1:] for tok in match.split(" ") if tok.startswith("@")]
            if len(listVariables) > 0:
                return listVariables[0]
            else:
                return None

        def find_facts_in_reponse(self,response):
            lowerResponse = response.lower()
            variable = None
            value = None

            # We replace multiwords city names by the name with _
            city = self.facts.containCity(lowerResponse)
            if city is not None:
                variable = "city"
                value = city.lower().replace(" ","_")
                lowerResponse = lowerResponse.replace(city.lower(),value)

            # We replace multiwords country names by the name with _
            country = self.facts.containCountry(lowerResponse)
            if country is not None:
                variable = "country"
                value = country.lower().replace(" ","_")
                lowerResponse = lowerResponse.replace(country.lower(),value)

            return variable,value,lowerResponse

        def match(self,matchString,variables,response):
            """
            Check if the user response match 1 of the possible answers
            """
            for tok,val in zip(matchString.split(" "),response.split(" ")):
                if tok.startswith("@"):
                    variable = tok[1:]
                    # Check if the variable match the fact base 
                    if "_" in variable:
                        if self.facts.checkFact(variable.split("_")[0], val.replace("_"," ")):
                            variables[variable] = val.replace("_"," ")
                            return True
                        else:
                            return False
                    else:
                        variables[variable] = val
                        return True
                elif tok != val:
                    return False
            return True

        def matchAnswer(self,state,variables,response):
            """
            Check all possible answers for the user response
            """
            _,_,lowerResponse = self.find_facts_in_reponse(response)
            for answer in self.states[state]["answers"]:
                if self.match(answer["match"],variables,lowerResponse):
                    return answer["goto"]
            return "dont_understand"

        def enumerateStates(self):
            """
            Return all states who has a description
            """
            for state,stateDefinition in self.states.items():
                if "description" in stateDefinition:
                    yield state,stateDefinition["description"]

        def enumerateAnswers(self,state):
            """
            Return all answers match and goto
            """
            for answer in self.states[state]["answers"]:
                yield answer["match"],answer["goto"]

        def addAnswer(self,state,response,goto):
            if "variable" in self.states[state]:
                variable = self.states[state]["variable"]
                if variable.startswith("@city"):
                    value = self.facts.containCity(response)
                elif variable.startswith("@country"):
                    value = self.facts.containCountry(response)
                else:
                    value = None
            else:
                value = None

            # Format the response
            if value is not None:
                match = response.lower().replace(value.lower(),variable)
            else:
                match = response

            # Add the answer
            self.states[state]["answers"].append({"match":match,"goto":goto})

        def randomMatch(self,question):
            state = question
            response = self.states[state]["answers"]
            dictionary = {}

            for key in response:
                data = key["match"]
                dictionary[data] = dictionary.get(data, "")

            if "exit" in dictionary:
                del dictionary["exit"]
            
            if "bye" in dictionary:
                del dictionary["bye"]
            
            if "" in dictionary:
                del dictionary[""]

            return random.choice(list(dictionary.keys()))

        # TODO
        # 1) In airport.csv variable correspond a @city
        # 2) Remplace @+variable in the response
        def randomAnswerV2(self,question,state):
            self.state = question
            response = self.states[self.state]["answers"]
            dictionary = {}

            for key in response:
                data = key["match"]
                dictionary[data] = dictionary.get(data, "")

            randAnswer = random.choice(list(dictionary.keys()))

            randomLetter = random.choice(string.ascii_uppercase)
            for variable in zip(randAnswer.split(" "),response.split(" ")):
                if "variable" in self.states[state]:
                    variable = self.states[state]["variable"]
                    if variable.startswith("@city"):
                        for city in self.facts.listCity():
                            if city.startswith(randomLetter):
                                value = city
                    elif variable.startswith("@country"):
                        for country in self.facts.listCountry():
                            if country.startswith(randomLetter):
                                value = country
                    else:
                        randomLetter = random.choice(string.ascii_uppercase)
                else:
                    value = None
        
            return value

        def randomAnswer(self,question,state):
            rdMatch = self.randomMatch(question)
            rdAnswer = self.facts.randomCity()

        def dumpKnowledge(self):
            """
            Create or Update if exist a Json file
            """
            json.dump(self.states,open("knowledgeDump.json","w"))

