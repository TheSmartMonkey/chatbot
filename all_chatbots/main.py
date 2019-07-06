### CHATBOT ###
# coding: utf8

import pandas as pa
import json
from copy import copy

from chatbot import Chatbot,KnowledgeBase
from chatbotScripted import Scripted
from chatbotFactBase import FactBase,testFacts
from chatbotFrend import ChatbotFrend


while __name__ == "__main__":
    bottype = input("1)scripted \n2)chatbot \n3)test the facts \n4)chatbot speeks with a chatbot frend \n5)exit \nWhich one do you want? ")
    if bottype == "1":
        Scripted("knowledgeBase.json").chat()
    elif bottype == "2":
        Chatbot("knowledgeDump.json").chat()
    elif bottype == "3":
        testFacts()
    elif bottype == "4":
        ChatbotFrend("knowledgeBase.json").chatWithAnotherChatbot()
    elif bottype == "5":
        break
    else:
        print("Retry")