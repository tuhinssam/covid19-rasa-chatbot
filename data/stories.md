## hospital search happy path
* greet
  - user_form
  - form{"name": "user_form"}
  - form{"name": null}
  - utter_how_can_i_help
* search_provider{"facility_type":"hospital", "location": "San Francisco"}
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
* inform{"location":"San Francisco"}
  - action_facility_search
  - utter_address
* thanks
  - utter_goodbye

## happy path 1
* greet
  - utter_how_can_i_help
* que-set-1
  - utter_que_set_1
* thanks
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye
