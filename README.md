# Documentation for Covid19-assist-bot

# COVID-19 interactive chatbot using Rasa
This chatbot is developed using RASA Framework. 

## What does this Robot is capable of?
- answer basic questions on COVID-19 like what, when, how, additionally it can handle smalltalk, chit-chat
- capable of answering questions like nearest tesing centers, Hospitals, Free food facility, nearby shelter homes
- Can provide statistics based on districts or states in India
- Send mail to the user with all the details
- stores entire chat in MongoDB database

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