# Documentation for Covid19-assist-bot

## covid19-assist-bot interactive chatbot using Rasa
This chatbot is developed using RASA Framework. 

## Why Rasa?
Rasa is an open source framework to develop assistant or chatbot. The most important difference between other chantbot frameworks like Google DialogFlow, MS LUIS and Rasa it that, in Rasa all the development, training and testing in Rasa can be done locally and data remains private to the organization or the user. You can select your model to train the data, make alterations if you are not satisfied with the result. In DialogFlow, LUIS all the development/training/testing is done in the provider's cloud environment. So you have to completely trust the provider about the data.

The downside of using Rasa is that, to develop assistant, one must have coding knowledge and understanding on the concepts of NLP (Natural Language Processing) 

## What does this Robot is capable of?
- answer basic questions on COVID-19 like what, when, how, additionally it can handle smalltalk, chit-chat
- capable of answering questions like nearest tesing centers, Hospitals, Free food facility, nearby shelter homes
- Can provide statistics based on districts or states in India
- Send mail to the user with all the details
- stores entire chat in MongoDB database

## Architecture

USER-->INTENT
INTENT--> STORY <-- UTTERENCE
  |            
ENTITY
INTENT--> STORY <--> CUSTOM ACTIONS & FORMS --> EXTERNAL API|DATABASE

## Database Being Used
MongoDB
DB Name: covid19db

language: "en"

## Actions and Forms
action_facility_search is used to query data from all external APIs to get details like hospitals, test centers, shelter homes, statistical information

user_form is used to track details from the user: name, email, mobile number, location

## Model Pipeline and Policies used

pipeline:
- name: "WhitespaceTokenizer"
- name: "RegexFeaturizer"
- name: "CRFEntityExtractor"
- name: "EntitySynonymMapper"
- name: "CountVectorsFeaturizer"
- name: "DIETClassifier"

# Configuration for Rasa Core.
policies:
  - name: MemoizationPolicy
    max_history: 3
    priority: 3
  - name: TEDPolicy
    max_history: 3
    epochs: 200
  - name: FallbackPolicy
    nlu_threshold: 0.3
    core_threshold: 0.3
    fallback_action_name: 'action_default_fallback'
  - name: MappingPolicy
  - name: FormPolicy

## Source Code GitHub Link:
all codes are available in GitHub Page: https://github.com/tuhinssam/covid19-rasa-chatbot

## How to run the project
 # create a virtual environment
 - pip install virtualenv
 - virtualenv rasavenv
 - activate the virtual environment: rasavenv/Scripts/Activate
 move to the virtual environment
 
 # install all the dependencies
 copy the requirements.txt in a folder
 install dependencies using following command:
 - pip install -r "requirements.txt" 

# Setup secret key and other configurations for integration with slack, facebook, telegram
Telegram integration: https://chatbotslife.com/full-tutorial-on-how-to-create-and-deploy-a-telegram-bot-using-python-69c6781a8c8f
Slack integration:  
 - train model: rasa train
 - train nlu: rasa train nlu
 - test interactive mode: rasa shell
 - run rasa using: rasa run
 - run actions server: rasa run actions



