## hospital search happy path
* greet
  - user_form
  - form{"name": "user_form"}
  - form{"name": null}
  - utter_how_can_i_help
* search_provider{"facility_type":"test center", "location": "bangalore"}
  - action_facility_search
  - utter_address
* thanks
  - utter_goodbye

## hospital search + location
* greet
  - user_form
  - form{"name": "user_form"}
  - form{"name": null}
  - utter_how_can_i_help
* search_provider{"facility_type":"hospital"}
  - utter_ask_location
* inform{"location":"karnataka"}
  - action_facility_search
  - utter_address
* thanks
  - utter_goodbye

## que_set_1
* que_set_1
  - utter_que_set_1
## que_set_2
* que_set_2
  - utter_que_set_2
## thanks
* thanks
  - utter_goodbye
## say goodbye
* goodbye
  - utter_goodbye
