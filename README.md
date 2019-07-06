# chatbot

Supinfo school project on the implementation of a chatbot

## What I learned

* How to setup a chatbot
* How to implemente an AI
* Learned basic concepts of AI like pathern matching
* Manipulate Json and CSV files
* Make an AI learn

## Getting started

1. Go to your project folder : ```cd "project_folder_path/chatbot/all_chatbots"```

2. Launch the script : ```python3 main.py```

3. Select you chatbot

![chatbot learn](https://raw.githubusercontent.com/TheSmartMonkey/myHome/master/images/chatbot_learn.png)

## Implemented AI

### chatbotScripted.py

Simplistic AI that follows the knowledge base at the letter: knowlageBase.json . It will only include the pre-formatted responses in our database.

### chatbot.py

Learning AI that updates his knowledge base every time that she's learning something: knowlageDump.json. When she doesn't know something, she'll
propose a suggestion list based on what she already knows. This way our AI will be able to evolve and become more and more intelligent as time goes by.

### chatbotFactBase.py

Simple script to test your facts. Modify at the end of the script to test the facts you want to test.

### chatbotFrend.py

Work in Progress

Is an AI that discusses with the Scripted AI that asks pre-formatted questions that it retrieves from the knowledge base: knowlageBase.json. Between each answer question there is a 5 second pause time to allow the user to see the conversations. If the bot who answers decides to end the conversation at that time, the user takes control of the application.
