## default path
* greet
  - utter_how_can_i_help
  - user_form
  - form{"name": "user_form"}
  - form{"name": null}
* search_provider{"facility_type":"test center"}
  - action_facility_search

## facility type test center
* search_provider{"facility_type":"test center"}
  - action_facility_search

## facility type hospital
* search_provider{"facility_type":"hospital"}
  - action_facility_search

## facilty type Shelter
* search_provider{"facility_type":"shelter homes"}
  - action_facility_search

## facilty type free food
* search_provider{"facility_type":"free food"}
  - action_facility_search

## facility statistics
* search_provider{"facility_type":"corona cases"}
  - action_facility_search

## facility email
* search_provider{"facility_type":"email"}
  - action_facility_search

## out_of_scope_story
* out_of_scope
  - utter_out_of_scope
## smalltalk_human_story
* smalltalk_human
  - utter_smalltalk_human
## faq_distancing_story
* faq_distancing
  - utter_faq_distancing
## faq_symptoms_story
* faq_symptoms
  - utter_faq_symptoms
## faq_vaccine_story
* faq_vaccine
  - utter_faq_vaccine
## faq_vulnerable_story
* faq_vulnerable
  - utter_faq_vulnerable
## faq_testing_story
* faq_testing
  - utter_faq_testing
## faq_supplies_story
* faq_supplies
  - utter_faq_supplies
## faq_whatisit_story
* faq_whatisit
  - utter_faq_whatisit
## thanks
* thanks
  - utter_thanks
## say goodbye
* goodbye
  - utter_goodbye
## mood_unhappy_story
* mood_unhappy
  - utter_cheer_up
